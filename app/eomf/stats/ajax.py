import json
from dajaxice.decorators import dajaxice_register

@dajaxice_register(method='GET')
def sayhello(request):
	return json.dumps({'message':'Hello World','extra':list(range(2000,2010))})