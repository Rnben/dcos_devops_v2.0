# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from dcos_devops.models import Host, Field, Cluster
from django.http import HttpResponse
import json
from django.db.models import Q
from django.contrib.auth.decorators import login_required


#@login_required(login_url="/login/")
def search_field(request):
    fields = []
    fields_query_res = Field.objects.all()
    for item in fields_query_res:
        fields.append(item.name)
    return render_to_response("show_host.html", {"fields": fields})


def search_cluster(request):
    clusters = []
    field = request.GET.get("field")
    field_id = Field.objects.filter(name=field)[0].id
    clusters_query_res = Cluster.objects.filter(field_id=field_id)
    for item in clusters_query_res:
        clusters.append(item.name)
    clusters_res = {"clusters": clusters}
    return HttpResponse(json.dumps(clusters_res), content_type='application/json')


def search_host(request):
    host_info = []
    cluster = request.GET.get("cluster")
    field = request.GET.get("field")
    if cluster != "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
        field_id = Field.objects.filter(name=field)[0].id
        cluster_id = Cluster.objects.filter(name=cluster, field_id=field_id)[0].id
        host_query_res = Host.objects.filter(cluster_id=cluster_id)
        for item in host_query_res:
            host_info.append({"field": field, "cluster": cluster, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
    elif cluster == "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
        field_id = Field.objects.filter(name=field)[0].id
        cluster_objs = Cluster.objects.filter(field_id=field_id)
        for item in cluster_objs:
            host_info_res = [host_obj for host_obj in Host.objects.filter(cluster_id=item.id)]
            for info in host_info_res:
                host_info.append({"field": field, "cluster": item.name, "name": info.name, "ip": info.ip, "comp_name": info.comp_name, "comp_port": info.comp_port})
    host_info_res = {"host_info": host_info}
    return HttpResponse(json.dumps(host_info_res), content_type='application/json')


def search_host_info(request):
    host_info = []
    cluster = request.GET.get("cluster")
    field = request.GET.get("field")
    if cluster != "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
        cluster_id = Cluster.objects.filter(name=cluster)[0].id
        search_info = request.GET.get("search_info")
        search_info_res = Host.objects.filter(
            Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(comp_port__contains=search_info),
            cluster_id=cluster_id)
        for item in search_info_res:
            host_info.append({"field": field, "cluster": cluster, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
    elif cluster == "--- 请选择集群约束 ---" and field != "--- 请选择生产域 ---":
        field_id3 = Field.objects.filter(name=field)[0].id
        search_info = request.GET.get("search_info")
        cluster_objs = Cluster.objects.filter(field_id=field_id3)
        for item in cluster_objs:
            search_info_res = [host_obj for host_obj in Host.objects.filter(
                Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(
                    comp_port__contains=search_info), cluster_id=item.id)]
            for info in search_info_res:
                host_info.append({"field": field, "cluster": item.name, "name": info.name, "ip": info.ip, "comp_name": info.comp_name, "comp_port": info.comp_port})
    else:
        search_info = request.GET.get("search_info")
        search_info_res = Host.objects.filter(
            Q(name__contains=search_info) | Q(ip__contains=search_info) | Q(comp_name__contains=search_info) | Q(comp_port__contains=search_info))
        for item in search_info_res:
            cluster_id2 = item.cluster_id
            cluster_obj = Cluster.objects.filter(id=cluster_id2)[0]
            field_id2 = cluster_obj.field_id
            cluster2 = cluster_obj.name
            field2 = Field.objects.filter(id=field_id2)[0].name
            host_info.append({"field": field2, "cluster": cluster2, "name": item.name, "ip": item.ip, "comp_name": item.comp_name, "comp_port": item.comp_port})
    host_info_res = {"host_info": host_info}
    return HttpResponse(json.dumps(host_info_res), content_type='application/json')

