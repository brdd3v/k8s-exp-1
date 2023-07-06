#!/usr/bin/env python

from constructs import Construct
from cdk8s import App, Chart
from imports import k8s


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        k8s.KubeDeployment(self, "fastapi_dep",
            metadata=k8s.ObjectMeta(name="fastapi"),
            spec=k8s.DeploymentSpec(
                replicas=3,
                selector=k8s.LabelSelector(match_labels={"app": "fastapi"}),
                template=k8s.PodTemplateSpec(
                    metadata=k8s.ObjectMeta(labels={"app": "fastapi"}),
                    spec=k8s.PodSpec(
                        containers=[
                            k8s.Container(
                                name="fastapi",
                                image="fastapi-app",
                                image_pull_policy="Never",
                                ports=[k8s.ContainerPort(container_port=8000)]
                            )
                        ]
                    )
                )
            )
        )

        k8s.KubeService(self, "fastapi_svc",
            metadata=k8s.ObjectMeta(name="fastapi"),
            spec=k8s.ServiceSpec(
                type="LoadBalancer",
                ports=[k8s.ServicePort(port=8000, 
                                       target_port=k8s.IntOrString.from_number(8000))],
                selector={"app": "fastapi"}
            )
        )

        k8s.KubeDeployment(self, "redis_dep",
            metadata=k8s.ObjectMeta(name="redis"),
            spec=k8s.DeploymentSpec(
                replicas=1,
                selector=k8s.LabelSelector(match_labels={"app": "redis"}),
                template=k8s.PodTemplateSpec(
                    metadata=k8s.ObjectMeta(labels={"app": "redis"}),
                    spec=k8s.PodSpec(
                        containers=[
                            k8s.Container(
                                name="redis",
                                image="redis:7.0-alpine",
                                ports=[k8s.ContainerPort(container_port=6379)]
                            )
                        ]
                    )
                )
            )
        )

        k8s.KubeService(self, "redis_svc",
            metadata=k8s.ObjectMeta(name="redis"),
            spec=k8s.ServiceSpec(
                type="ClusterIP",
                ports=[k8s.ServicePort(port=6379)],
                selector={"app": "redis"}
            )
        )


app = App()
MyChart(app, "cdk8s")

app.synth()
