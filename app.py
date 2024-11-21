
from flask import Flask, jsonify
from kubernetes import client, config

app = Flask(__name__)

@app.route('/pods', methods=['GET'])
def get_pods():
    try:
        # Load the Kubernetes config from the local environment (Minikube)
        # config.load_kube_config(config_file="/home/springleo/.kube/config")
        # config.load_kube_config()
        config.load_incluster_config()

        # Initialize the Kubernetes API client
        v1 = client.CoreV1Api()

        # Fetch all pods in the default namespace
        pods = v1.list_pod_for_all_namespaces(watch=False)
        pod_list = [
            {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
            }
            for pod in pods.items
        ]

        return jsonify({"pods": pod_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

