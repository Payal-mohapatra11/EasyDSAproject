from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

client = Groq(api_key=settings.GROQ_API_KEY)

DSA_KEYWORDS = [
    "array", "linked list", "stack", "queue", "tree", "graph",
    "binary search", "linear search", "sorting", "recursion", "dynamic programming",
    "dp", "greedy", "hash", "heap", "trie", "backtracking",
    "time complexity", "space complexity", "dsa","algorithm", "data structure","searching","search",
    "bubble sort", "selection sort", "insertion sort",
    "merge sort", "quick sort", "heap sort",
    "counting sort", "radix sort", "bucket sort", "hashmap", "hash set", "hash table", "priority queue", "disjoint set", "union find",
]

def is_dsa_question(question: str) -> bool:
    q = question.lower()
    return any(keyword in q for keyword in DSA_KEYWORDS)

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
         # HARD FILTER (very important)
        if not is_dsa_question(question):
            return JsonResponse({
                "answer": (
                    "I only answer Data Structures and Algorithms (DSA) questions.\n\n"
                    "Please ask about arrays, linked lists, trees, graphs, sorting, etc."
                )
            })
        
        response = client.chat.completions.create(model="llama-3.1-8b-instant",messages=[ { 
           
                    "role": "system",
                    "content": (
                        "You are EasyDSA Tutor, a strict Data Structures and Algorithms assistant.\n"
                        "RULES:\n"
                        "1. Only answer DSA-related questions.\n"
                        "2. If the question is not about DSA, refuse politely.\n"
                        "3. Explain step-by-step.\n"
                        "4. Always include time and space complexity when applicable.\n"
                        "5. Provide code in Java, C++, or Python when coding is required.\n"
                        "6. Keep answers clear and beginner friendly.\n"
                    )
        },
             {
              "role":"user",
              "content": question
          }                                                                      
        ],
          
          temperature=0.3
          
          )
        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})
    
    return JsonResponse({"error":"Invalid request method."},status=400)
        