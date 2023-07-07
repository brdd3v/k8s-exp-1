"""A Kubernetes Python Pulumi program"""

from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service


fastapi_development = Deployment(
    "fastapi",
    metadata={"name": "fastapi"},
    spec={
        "replicas": 3,
        "selector": {
            "match_labels": {"app": "fastapi"}
        },
        "template": {
            "metadata": {
                "labels": {"app": "fastapi"}
            },
            "spec": {
                "containers": [
                    {"name": "fastapi", 
                     "image": "fastapi-app",
                     "image_pull_policy": "Never",
                     "ports": [{"container_port": 8000}]
                    }
                ]
            }
        }
    }
)


fastapi_service = Service(
    "fastapi",
    metadata={"name": "fastapi"},
    spec={
        "selector": {"app": "fastapi"},
        "ports": [{"port": 8000, 
                   "target_port": 8000}],
        "type": "LoadBalancer"
    }
)


redis_development = Deployment(
    "redis",
    metadata={"name": "redis"},
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {"app": "redis"}
        },
        "template": {
            "metadata": {
                "labels": {"app": "redis"}
            },
            "spec": {
                "containers": [
                    {"name": "redis",
                     "image": "redis:7.0-alpine",
                     "ports": [{"container_port": 6379}]
                    }
                ]
            }
        }
    }
)


redis_service = Service(
    "redis",
    metadata={"name": "redis"},
    spec={
        "selector": {"app": "redis"},
        "ports": [{"port": 6379}],
        "type": "ClusterIP"
    }
)

