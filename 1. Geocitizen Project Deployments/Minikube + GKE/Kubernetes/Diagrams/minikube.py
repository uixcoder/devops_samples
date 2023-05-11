from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github
from diagrams.onprem.network import Tomcat
from diagrams.onprem.client import User
from diagrams.programming.language import Java
from diagrams.custom import Custom
from diagrams.k8s.compute import Pod
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import RS
from diagrams.k8s.network import SVC
from diagrams.k8s.infra import Node
from diagrams.onprem.client import Client
from diagrams.k8s.controlplane import API


with Diagram("Geocitizen Application Minikube Infrastructure", show=False):

    with Cluster("minikube"):
        node = API("")
        with Cluster("Deployment geo-deployment-autoscaling"):
            hpa = HPA("HorizontalPodAutoscaler")
            replica = RS("Replica Set")
            with Cluster("Replica N"):
                app_podN = Pod("Pod N")
                with Cluster(""):
                    tN = Tomcat("Tomcat 9")
                    geoappN = Custom("Geocitizen", "./img/geo.png")
        with Cluster("Deployment geo-deployment-postgres"):
            db_pod = Pod("Pod DB")
            with Cluster(""):
                database = PostgreSQL("Database")
        s_db = SVC("geo-db-pod-service\nNodePort\n10.110.99.99:5432")
        s_app = SVC(
            "geo-app-pod-service\nLoadBalancer\n10.107.140.122\n80<->8080")

    node - Edge(color="red", style="bold") >> [hpa, db_pod, s_app, s_db]
    (hpa >> replica >> app_podN)
    app_podN >> tN >> geoappN
    db_pod >> database
    geoappN >> s_db >> db_pod
    s_app - Edge(tailport="ne", headport="sw", minlen="2") >> hpa

    with Cluster("Service PC"):
        jav = Java("")
        mvn = Custom("", "./img/maven.png")
        Jen = Jenkins()
        docker_image = Custom("Custom docker image", "./img/docker.png")

    Dev = User("DevOps")
    repo = Github("Application repository")

    with Cluster("Docker Hub"):
        docker_hub_private = Custom(
            "Docker hub \n(private)", "./img/docker2.png")
        docker_hub_open = Custom("Docker hub \n(open)", "./img/docker2.png")
    Jen >> mvn >> Edge(
        headport="nw", tailport="se") >> docker_image >> docker_hub_private
    repo >> Edge(headport="nw", tailport="se") >> Jen
    mvn >> jav

    (Dev - Edge(color="red", fontsize="20", tailport="se", headport="nw", minlen="1",
                style="bold") - node)
    docker_hub_private >> Edge(
        color="red", xlabel="", style="bold") >> app_podN
    docker_hub_open >> Edge(
        color="red", fontsize="20", xlabel="1 step\nkubectl apply -f db.yml\nkubectl apply -f app.yml", style="bold") >> db_pod

    Dev - Edge(color="green", fontsize="20", tailport="ne", headport="sw", minlen="2",
               xlabel="2 step\nget IPs\nrun pipeline", style="bold") >> Jen
    b = Node("", shape="plaintext", height="0.0", width="0.0")
    docker_hub_private >> Edge(
        color="blue", style="bold") >> app_podN
    Dev >> Edge(tailport="s", headport="s",
                color="blue", fontsize="20", xlabel="3 step\nupdate docker image", style="bold") >> app_podN

    client = Client("Web browser")
    client - Edge(color="black", fontsize="16",
                  xlabel="", style="bold") >> s_app
