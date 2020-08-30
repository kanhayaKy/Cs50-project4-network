document.addEventListener('DOMContentLoaded', function() {
    postForm = document.querySelector('#new-post-form');
    if(postForm!=null){
        postForm.onsubmit = () => createPost();
    }

    followButton = document.querySelector('.follow-button');
    if(followButton)
        followButton.addEventListener('click',()=>follow(followButton.dataset.user_id))


    likeButton = document.querySelectorAll('#like-button');
    if(likeButton){
            likeButton.forEach(button => {
                button.addEventListener('click', event=>likePost(event,button.dataset.post_id))

            });

    }

    editButton = document.querySelectorAll('#edit-button');
    if(editButton){
        editButton.forEach(button => {
            button.addEventListener('click', () =>{
                editPost(button.dataset.post_id);

            } )
        })
    }

});

function editPost(postId){
    post = document.getElementById(`${postId}`);
    post.querySelector("#edit-button").classList.add("d-none")
    post.querySelector(".card-body").classList.add("d-none");
    post.querySelector(".edit-form").classList.remove("d-none")
    post.querySelector("#save-button").addEventListener('click', () => {
        console.log("saved");
        fetch(`/like/${postId}`,{
            method:'POST',
            body: JSON.stringify({
                body: post.querySelector("#text-body").value
            })
        })
        .then(response => response.json())
        .then(result => {
            //console.log(result);
            post.querySelector(".card-title").innerText = result["body"];
        })
        post.querySelector("#edit-button").classList.remove("d-none")
        post.querySelector(".card-body").classList.remove("d-none");
        post.querySelector(".edit-form").classList.add("d-none")
    })

   

}



function likePost(event,postId){
    like = event.target.firstElementChild;
    if (like.classList.contains("fas"))
        like.classList.replace("fas" , "far");
    else
        like.classList.replace("far" , "fas");

    console.log(event.target.firstElementChild.classList);

    fetch(`/like/${postId}`,{
        method:'PUT',
        
    })
    .then(response => response.json())
    .then(result => {
        event.target.lastElementChild.innerText = result['count'];

    })
}

function follow(userId){
    fetch(`/user/${userId}`,{   
        method:'PUT',
    })
    .then(response => response.json())
    
    .then(result => {
            if(result["following"]){
                followButton.innerText = "Unfollow";
                document.querySelector(".followers").innerText = `${result["count"]} followers`;
            }
            else{
                followButton.innerText = "Follow";
                document.querySelector(".followers").innerText = `${result["count"]} followers`;
            }
            
    })
}


function createPost(){
    fetch('/post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-body').value
        })
      })
      .then(response => response.json())
      .then(result => {
          setTimeout(()=>{
              location.reload();
          },500);
     
          document.querySelector(".alert").classList.remove("d-none");
          setTimeout(() => {
            document.querySelector(".alert").classList.add("d-none");

          }, 3000);
      });
      document.querySelector('#post-body').value = "";
      return false;
}
