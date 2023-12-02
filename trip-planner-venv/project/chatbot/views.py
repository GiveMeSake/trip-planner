from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
import openai

def input_validation(request):
    validationText = request.POST.get('validationText', '')
    
    openai.api_key = "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"

    print(validationText)
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": validationText}
        ]
    )

    is_valid = completion.choices[0].message.content

    return JsonResponse({'isValid': is_valid})

def show_results(request):
    if request.method == 'POST':
        # Parse the JSON data from the request
        final_prompt = request.POST.get('finalPrompt', '')
    
        openai.api_key = "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"

        print(final_prompt)
        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role": "Act as a trip planner", "content": final_prompt}
            ]
        )

        final_result = completion.choices[0].message.content
        print(final_result)

        # Redirect to another page after processing
        return render(request, 'result_page.html') # Replace with the URL you want to redirect to

    else:
        # Handle non-POST requests if necessary
        return JsonResponse({'error': 'Invalid request'}, status=400)
    





