# 1) bootstrap
sudo bash scripts/00-bootstrap-bastion.sh

# 2) harden (set your actual bastion login user)
sudo BASTION_USER=adminuser bash scripts/10-hardening.sh

# 3) pull kubeconfig
bash scripts/20-kubeconfig-sync.sh

# 4) verify cluster access
kubectl get nodes -o wide
