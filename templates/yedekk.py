def add_to_like(request, slug):
    item = get_object_or_404(Post, slug=slug)
    if item.likes.filter(id=request.user.id): #already liked the content
        item.likes.remove(request.user) #remove user from likes 
        liked=False
    else:
        item.likes.add(request.user)
        liked=True
    return redirect("post-detail",slug=slug)