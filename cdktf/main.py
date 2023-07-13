#!/usr/bin/env python

from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_kubernetes.provider import KubernetesProvider
from cdktf_cdktf_provider_kubernetes import (
    deployment,
    service
)


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        KubernetesProvider(self, "Kubernetes",
                           config_path="~/.kube/config",
                           config_context="minikube")
        
        deployment.Deployment(self, "fastapi_deploy",
                            metadata=deployment.DeploymentMetadata(name="fastapi"),
                            spec=deployment.DeploymentSpec(
                                replicas="3",
                                selector=deployment.DeploymentSpecSelector(match_labels={"app": "fastapi"}),
                                template=deployment.DeploymentSpecTemplate(
                                    metadata=deployment.DeploymentSpecTemplateMetadata(labels={"app": "fastapi"}),
                                    spec=deployment.DeploymentSpecTemplateSpec(container=[
                                        deployment.DeploymentSpecTemplateSpecContainer(
                                        name="fastapi", 
                                        image="fastapi-app", 
                                        image_pull_policy="Never", 
                                        port=[
                                            deployment.DeploymentSpecTemplateSpecContainerPort(container_port=8000)
                                        ])
                                    ])
                                )    
                            ))

        service.Service(self, "fastapi_svc",
                        metadata=service.ServiceMetadata(name="fastapi"),
                        spec=service.ServiceSpec(
                            selector={"app": "fastapi"},
                            type="LoadBalancer",
                            port=[
                                service.ServiceSpecPort(port=8000,
                                                        target_port="8000")
                            ]
                        ))

        deployment.Deployment(self, "redis_deploy",
                            metadata=deployment.DeploymentMetadata(name="redis"),
                            spec=deployment.DeploymentSpec(
                            replicas="1",
                            selector=deployment.DeploymentSpecSelector(match_labels={"app": "redis"}),
                            template=deployment.DeploymentSpecTemplate(
                                metadata=deployment.DeploymentSpecTemplateMetadata(labels={"app": "redis"}),
                                spec=deployment.DeploymentSpecTemplateSpec(container=[
                                    deployment.DeploymentSpecTemplateSpecContainer(
                                        name="redis",
                                        image="redis:7.0-alpine",
                                        port=[
                                            deployment.DeploymentSpecTemplateSpecContainerPort(container_port=6379)
                                        ])
                                ])
                            )     
                            ))

        service.Service(self, "redis_svc",
                        metadata=service.ServiceMetadata(name="redis"),
                        spec=service.ServiceSpec(
                            selector={"app": "redis"},
                            type="ClusterIP",
                            port=[
                                service.ServiceSpecPort(port=6379,
                                                        target_port="6379")
                            ]
                        ))


app = App()
MyStack(app, "cdktf")

app.synth()
