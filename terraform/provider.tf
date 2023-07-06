terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.21.1"
    }
  }

  required_version = "~> 1.4.1"
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}
