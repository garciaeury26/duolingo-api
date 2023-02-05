from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import duolingo
import json
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt;
from django.views.decorators.http import require_http_methods;

@require_http_methods(["GET"])
def index(request):
    return HttpResponse('hola mundo');

@require_http_methods(['GET'])
def getCookie(request):
    if request.method == 'GET':
      csrf_token = request.META.get('CSRF_COOKIE', '');
      return JsonResponse({
          "ok":True,
          "token":csrf_token
      })
    else:
        return JsonResponse({
            "msg":'No se acpetan peticiones POST'
        })

@require_http_methods(['POST'])
#@ensure_csrf_cookie
# con esto activo no es necesario mandar cookies
@csrf_exempt
def getUserInfo(request):
        
    body = json.loads(request.body.decode('utf-8'));
    print(body)
      
    try:
        lingo = duolingo.Duolingo(body['user'], body['password'])
        return JsonResponse(lingo.get_user_info())
    except:
        return HttpResponse('Ha ocurrido un error')
 
        
@require_http_methods(['POST'])
@csrf_exempt
def getAudioUrl(request):
    
    body = json.loads(request.body.decode('utf-8'));
    lingo = duolingo.Duolingo(body['user'], body['password']);
    
    if not lingo:
        return JsonResponse({
            "msg":'El usuario no existe',
            "ok":False
        })
        
    audio = lingo.get_audio_url('hello');
    print(audio)
    
    return JsonResponse({
        "msg":'Audio de la palabra',
        "ok":True,
        "audio":audio
    })

    

   