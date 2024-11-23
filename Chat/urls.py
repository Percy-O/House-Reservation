from django.conf.urls import url,include
from Chat import views


app_name = 'Chat'

urlpatterns = [
	url(r'^chat/message/$',views.tenantMessage,name="tenant_message"),
	url(r'^chat/message/(?P<pk>[\d]+)/$',views.tenantMessageview,name="tenant_message_view"),
	url(r'^all/chat/message/$',views.allTenantChat,name="all_tenant_message"),

	url(r'^chat/message/(?P<house>[A-Za-z \s]+)/$',views.agentMessage,name="agent_message"),
	url(r'^all/chat/message/$',views.allAgentChat,name="all_agent_message"),


]