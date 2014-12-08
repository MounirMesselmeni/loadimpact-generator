http.set_max_connections({{ num_threads }}, {{ num_threads }})

http.request_batch({
{% for test in tests %}
    {"{{ test.method }}", "{{ test.url }}" {% if test.auto_redirect %}auto_redirect=true,{% endif %}},
{% endfor %}
})