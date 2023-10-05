document.addEventListener('DOMContentLoaded', function() {

    view_posts("all");
  });


function view_posts(username) {

    fetch(`/view_posts/${username}`)
    .then(response => response.json())
    .then(posts => {

      const postList = document.querySelector('#posts');

      // Loop through each post and create HTML elements
      posts.forEach(post => {

            var element = document.createElement("div");
            element.innerHTML =
                `
                <div class="post">
                    <div class="avatar">
                        <h1>❍</h1>
                    </div>
                    <div>
                        <div class="post_details">
                            <strong>
                                <a href="/${post.user}">${post.user}</a>
                            </strong>
                            <div class="post_time">${post.time}</div>
                        </div>
                        <div class="post_content">${post.content}</div>
                        <div class="like_display">
                            <div>
                                <button id="like_button_${post.id}"></button>
                            </div>
                            <div>
                                <p id="like_count_${post.id}">${post.like_count}</p>
                            <div>
                        </div>
                    </div>
                </div>
                `;
                postList.append(element);

                // Fetches whether the post is already liked by the user (true / false)
                fetch(`/like/${post.id}`)
                .then(response => response.json())
                .then(liked => {
                    button = document.getElementById(`like_button_${post.id}`)

                    if (liked == true) {
                        // onclick the button will trigger the like function, passing on the true/false status of previous likes
                        button.setAttribute("onclick", `like(${post.id}, true)`)
                        button.innerHTML = "💚"
                    }
                    else {
                        button.setAttribute("onclick", `like(${post.id}, false)`)
                        button.innerHTML = "🤍"
                    }
                })

          })
      })
}

function like(post_id, liked) {

    like_counter = document.getElementById(`like_count_${post_id}`)
    button = document.getElementById(`like_button_${post_id}`)

    // if the post was previously liked, decrease the like count, change the button properties to "unliked"
    if (liked == true) {
        like_counter.innerHTML--
        button.innerHTML = "🤍"
        button.setAttribute("onclick", `like(${post_id}, false)`)
        data = -1
    }
    // if the post was not previously liked, increase the like count, change the button properties to "liked"
    else {
        like_counter.innerHTML++
        button.innerHTML = "💚"
        button.setAttribute("onclick", `like(${post_id}, true)`)
        data = 1
    }
    // sends a PUT request to the API to update the like count via the data above (+1 or -1)
    fetch(`/like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like_count: data,
        }),
    })
}