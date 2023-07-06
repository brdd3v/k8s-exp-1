resource "kubernetes_deployment" "fastapi" {
  metadata {
    name = "fastapi"
  }
  spec {
    replicas = 3
    selector {
      match_labels = {
        app = "fastapi"
      }
    }
    template {
      metadata {
        labels = {
          app = "fastapi"
        }
      }
      spec {
        container {
          name              = "fastapi"
          image             = "fastapi-app"
          image_pull_policy = "Never"
          port {
            container_port = 8000
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "fastapi" {
  metadata {
    name = "fastapi"
  }
  spec {
    selector = {
      app = kubernetes_deployment.fastapi.spec.0.template.0.metadata.0.labels.app
    }
    type = "LoadBalancer"
    port {
      port        = 8000
      target_port = 8000
    }
  }
}
