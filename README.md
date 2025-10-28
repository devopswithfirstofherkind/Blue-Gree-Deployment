# 🌀 Blue-Green Deployment with NGINX Reverse Proxy

This setup demonstrates a **Blue-Green Deployment** pattern using **Docker Compose**.  
Two identical Node.js apps (`blue` and `green`) run on separate containers, and an **NGINX reverse proxy** routes traffic between them.

---

## 🚀 Project Structure

Blue-Gree-Deployment/
├── docker-compose.yml
├── nginx.conf.template
├── entrypoint.sh
├── README.md


---

## ⚙️ Prerequisites

- Docker and Docker Compose installed
- Port **8080**, **8081**, and **8082** available
- Node.js app image already built (or pulled)

---


---

## ⚙️ How It Works

- **Blue** and **Green** containers** run identical applications on different ports (8081 & 8082).  
- **Nginx** acts as a reverse proxy, routing all requests to the active pool.  
- The environment variable `ACTIVE_POOL` determines which app receives traffic.  
- The configuration file `/etc/nginx/nginx.conf` is generated dynamically from `nginx.conf.template` at container startup.  
- A chaos endpoint (`/chaos/start?mode=error`) can simulate downtime for testing failover.

---

## 🚀 Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Blue-Gree-Deployment.git
   cd Blue-Gree-Deployment
2. **Start all containers:**

   ```bash
   docker-compose up -d

3. Access the applications:

Nginx (proxy): http://localhost:8080
Blue app: http://localhost:8081
Green app: http://localhost:8082

4. **⚡ Chaos Testing (Simulated Downtime)**

To simulate downtime in one of the app containers:

curl -X POST http://localhost:8081/chaos/start?mode=error


🧠 Notes

If deploying across multiple instances, replace app names (app_blue, app_green) in nginx.conf.template with their instance private IPs.

Ensure all instances are reachable on the same network (VPC or custom bridge network).

Always verify connectivity before testing with:

curl http://<APP_IP>:8080/version


ENJOYYY!!!!!!!!











