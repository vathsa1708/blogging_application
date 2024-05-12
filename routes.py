from fastapi import APIRouter, HTTPException
from bson import ObjectId  # Import ObjectId to convert post_id string to ObjectId
from model import Post, CreatePost, UpdatePost, Comment, LikeDislike
from database import db
from typing import Optional
from datetime import datetime
from pydantic import ValidationError


router = APIRouter()

# Create a new post
@router.post("/posts/")
def create_new_post(post: CreatePost):
    post_id = db.get_collection("posts").insert_one(post.model_dump()).inserted_id
    return {"post_id": str(post_id)}

# Get a post by ID

@router.get("/posts/{post_id}")
def read_post(post_id: str):
    try:
        # Convert post_id string to ObjectId
        post_obj_id = ObjectId(post_id)
        post_data = db.get_collection("posts").find_one({"_id": post_obj_id})
        if post_data:
            return Post(**post_data)
        else:
            raise HTTPException(status_code=404, detail="Post not found")
    except ObjectId.InvalidId:
        print("Invalid Post ID")
        raise HTTPException(status_code=400, detail="Invalid Post ID")
@router.get("/all_posts/")  
def read_all_posts():
    try:
        posts_data = db.get_collection("posts").find()
        posts = []
        for post_data in posts_data:
            try:
                post = Post(**post_data)
                posts.append(post)
            except ValidationError as ve:
                print(f"Validation error when creating Post object: {ve}")
                # Log the validation error and continue to the next post
            except Exception as e:
                print(f"An error occurred while processing a post: {e}")
                # Log the error and continue to the next post
        return posts
    except Exception as e:
        print(f"An error occurred while fetching all posts: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



# Update a post
@router.put("/posts/{post_id}")
def update_post(post_id: str, post: UpdatePost):
    # Convert post_id string to ObjectId
    post_obj_id = ObjectId(post_id)
    # Update the post with the new data
    result = db.get_collection("posts").update_one({"_id": post_obj_id}, {"$set": post.model_dump()})
    if result.modified_count == 1:
        return {"message": "Post updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Delete a post
@router.delete("/posts/{post_id}")
def delete_post(post_id: str):
    # Convert post_id string to ObjectId
    post_obj_id = ObjectId(post_id)
    result = db.get_collection("posts").delete_one({"_id": post_obj_id})
    if result.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Add a comment to a post
@router.post("/posts/{post_id}/comments/")
def add_comment_to_post(post_id: str, comment: Comment):
    # Convert post_id string to ObjectId
    post_obj_id = ObjectId(post_id)
    result = db.get_collection("posts").update_one({"_id": post_obj_id}, {"$push": {"comments": comment.dict()}})
    if result.modified_count == 1:
        return {"message": "Comment added successfully"}
    else:
        raise HTTPException(status_code=404, detail="Post not found")

# Like or dislike a post
@router.post("/posts/{post_id}/like-dislike/")
def like_dislike_post(post_id: str, action: LikeDislike):
    # Convert post_id string to ObjectId
    post_obj_id = ObjectId(post_id)
    
    if action.action == 'like':
        db.get_collection("posts").update_one({"_id": post_obj_id}, {"$inc": {"likes": 1}})
        return {"message": "Post liked successfully"}
    elif action.action == 'dislike':
        db.get_collection("posts").update_one({"_id": post_obj_id}, {"$inc": {"dislikes": 1}})
        return {"message": "Post disliked successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action, action must be 'like' or 'dislike'")
