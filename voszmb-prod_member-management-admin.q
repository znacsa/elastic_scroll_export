{
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "container.labels.com_docker_swarm_service_name": "voszmb-prod_member-management-admin"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "now-24h/h",
              "lte": "now"
            }
          }
        }
      ]
    }
  }
}
