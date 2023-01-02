import os
#kubectl required

wdir=os.getcwd()

def istio_installation():
    istio_dir = os.path.join(wdir,"istio-1.16.1")  
    os.chdir(istio_dir)
    bin_dir = os.path.join(istio_dir,"bin")
    #export 'PATH=${bin_dir}:$PATH"
    os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"
    os.system("kubectl create ns istio-system")
    os.system("istioctl install")
    os.system("kubectl label namespace default istio-injection=enabled")   

def kiali_setup():
    kiali_dir = "istio-1.16.1/samples/addons/"
    kiali_dir = os.path.join(wdir, kiali_dir)
    os.chdir(kiali_dir)
    os.system("kubectl create -f kiali.yaml")
    os.system("kubectl create -f prometheus.yaml")


def set_up_argocd():
    os.chdir(wdir)
    os.system("kubectl create ns argocd")
    os.system("kubectl apply -f ./argo-cd-install.yaml -n argocd")
    # changing the arocd UI service type to load balancer
    # kubectl patch svc   argocd-server -n argocd -p '{'spec': {'type': 'LoadBalancer'}}'
    os.system("kubectl patch svc argocd-server -n argocd -p '{\"spec\": {\"type\": \"LoadBalancer\"}}'")
    # after that login with password

def set_up_argo_rollout():
    os.chdir(wdir)
    os.system("kubectl create ns argo-rollouts")
    os.system("kubectl apply -n argo-rollouts -f argo-rollout-install.yaml")

def creating_autosync_application():
    os.chdir(wdir)
    os.system("kubectl create -f argocd-auto-sync.yaml")

# istio_installation()
# kiali_setup()
set_up_argocd()
set_up_argo_rollout()
creating_autosync_application()
