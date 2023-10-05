document.addEventListener('DOMContentLoaded', function() {

    // By default, load the inbox
    view_posts();
  });


function view_posts() {

    fetch(`/view_posts`)
    .then(response => response.json())
    .then(posts => {

      const postList = document.querySelector('#posts');

      // Loop through each post and create HTML elements
      posts.forEach(post => {

            var element = document.createElement("div");
            element.innerHTML =
                `
                <div class="post">
                    <div class="post_details">
                        <h1>❍</h1>
                    </div>
                    <div>
                        <strong>${post.user}</strong>
                        <div>${post.time}</div>
                    </div>
                    <div>${post.content}</div>
                    <div class="like_display">
                        <button id="like_button_${post.id}"></button>
                        <p id="like_count_${post.id}">${post.like_count}</p>
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