from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import openai

def input_validation(request):
    input_to_validate = request.POST.get('input_to_validate', '')
    
    openai.api_key = "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"

    try:
        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Is {input_to_validate} a valid and unique location in United State? Answer 0 for no, 1 for yes"}
            ]
        )
        print(completion)
    except:  
        print("Error")
    

    
    is_valid = completion.choices[0].message.content
    print(is_valid)

    return JsonResponse({'isValid': is_valid})

