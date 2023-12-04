from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.conf import settings
import openai
import re
def input_validation(request):
    validationText = request.POST.get('validationText', '')
    
    openai.api_key = settings.OPENAI_API_KEY

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
    
        openai.api_key = settings.OPENAI_API_KEY

        match = re.search(r'to\s+(.*?)\s+for', final_prompt)
        if match:
            destination = match.group(1).strip()
        match = re.search(r'for\s+(\d+)\s+people', final_prompt)
        if match:
            numOfPeople = match.group(1).strip()

        request.session['destination'] = destination
        request.session['numOfPeople'] = numOfPeople
        print(destination)
        print(numOfPeople)
        print(final_prompt)
        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role":"assistant", "content": final_prompt}
            ]
        )

        final_result = completion.choices[0].message.content
        request.session['final_result'] = final_result
        # Redirect to another page after processing
        return render(request, 'result_page.html') # Replace with the URL you want to redirect to

    else:
        # Handle non-POST requests if necessary
        return JsonResponse({'error': 'Invalid request'}, status=400)