from app.tools.web_search import search_tool


query = "Generative AI applications in healthcare"


results = search_tool.invoke({
    "query": query
})


print("\n==============================")
print("WEB SEARCH RESULTS")
print("==============================")

print(results)