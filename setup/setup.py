import os
#kubectl required
def set_up_argocd():
    os.system("kubectl create ns argocd")
    os.system("kubectl apply -f ./argo-cd-install.yaml -n argocd")
    # changing the arocd UI service type to load balancer
    # kubectl patch svc   argocd-server -n argocd -p '{'spec': {'type': 'LoadBalancer'}}'
    os.system("kubectl patch svc argocd-server -n argocd -p '{\"spec\": {\"type\": \"LoadBalancer\"}}'")
    # after that login with password

def set_up_argo_rollout():
    os.system("kubectl create ns argo-rollouts")
    os.system("kubectl apply -n argo-rollouts -f argo-rollout-install.yaml")

def creating_autosync_application():
    os.system("kubectl create -f argocd-auto-sync.yaml")

set_up_argocd()
set_up_argo_rollout()
creating_autosync_application()
