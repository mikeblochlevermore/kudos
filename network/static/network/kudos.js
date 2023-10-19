document.addEventListener('DOMContentLoaded', function() {

    // Get the current path from the URL
    const currentPath = window.location.pathname;

    // Get the current page from the URL (default is page = 1)
    let page = new URLSearchParams(window.location.search).get("page") || 1;

    // If the current url is the index, view_posts("all")
    if (currentPath === "/") {
        view_posts("all", page);
    } else if (currentPath === "/following") {
        view_posts("following", page);
    }
    else {
        // If the current url contains a username, run view_posts("username")
        // Note: "substring(1)" removes the "/" from e.g. "/mike"
        const pathSegments = currentPath.split('/');
        const username = pathSegments[pathSegments.length - 1];
        view_posts(username, page)

        // setup the follow button

        fetch(`/profile/${username}/follow`)
        .then(response => response.json())
        .then(followed => {

            const follow_button_div = document.getElementById("follow_button_div");
            const button = follow_button_div.querySelector("button");

            if (followed == true) {
                // onclick the button will trigger the like function, passing on the true/false status of previous likes
                button.setAttribute("onclick", `follow('${username}', true)`)
                button.innerHTML = "Following"
                button.setAttribute("id", "unfollow_button");
            }
            else {
                button.setAttribute("onclick", `follow('${username}', false)`)
                button.innerHTML = "Follow"
                button.setAttribute("id", "follow_button");
            }
        })
    }
  });


function view_posts(filter, page) {

    // Options for the "filter" variable:
    // "all" to view all posts
    // "following" to see posts from people the user is following
    // "{username}" to see posts from just that specific user

    fetch(`/view_posts/${filter}/${page}`)
    .then(response => response.json())
    .then(posts => {

      const postList = document.querySelector('#posts');

      // Loop through each post and create HTML elements
      posts.forEach(post => {

        console.log(post)

            var element = document.createElement("div");
            element.innerHTML =
                `
                <div class="post">
                    <div class="post_wrapper">
                        <div>
                            <img class="avatar" src="${post.bio_image}">
                        </div>
                        <div>
                            <div class="post_details">
                                <strong>
                                    <a href="/profile/${post.user}">${post.user}</a>
                                </strong>
                                <div class="post_time">
                                    ${post.time}
                                </div>
                            </div>
                            <div class="post_content">
                                ${post.content}
                            </div>
                            <div>
                                <img class="post_image" src=${post.image_url}>
                            </div>
                            <div class="like_display">
                                <div>
                                    <button
                                        onclick="like(${post.id}, ${post.liked})"
                                        id="like_button_${post.id}">
                                        🙌
                                    </button>
                                </div>
                                <div>
                                    <p id="like_count_${post.id}">${post.like_count}</p>
                                <div>
                            </div>
                        </div>
                    </div>
                </div>
                `;
                postList.append(element);

                // Set the like button styling based on whether the post is already liked by the current user
                // Onclick triggers the like(post.id, post.liked) function, passing on the id and the true/false status of previous likes

                button = document.getElementById(`like_button_${post.id}`)
                if (post.liked == true) {
                    button.style.color = "black";
                    button.style.textShadow = "none";
                }
                else {
                    button.style.color = "transparent";
                    button.style.textShadow = "0 0 0 lightgray";
                }
          })
      })
}

function like(post_id, liked) {

    like_counter = document.getElementById(`like_count_${post_id}`)
    button = document.getElementById(`like_button_${post_id}`)

    // if the post was previously liked, decrease the like count, change the button properties to "unliked"
    if (liked == true) {
        like_counter.innerHTML--
        button.style.color = "transparent";
        button.style.textShadow = "0 0 0 lightgray";
        button.setAttribute("onclick", `like(${post_id}, false)`)
        data = -1
    }
    // if the post was not previously liked, increase the like count, change the button properties to "liked"
    else {
        like_counter.innerHTML++
        button.style.color = "black";
        button.style.textShadow = "none";
        button.setAttribute("onclick", `like(${post_id}, true)`)
        data = 1
    }
    // sends a PUT request to the API:
    // - updates the like count via the data above (+1 or -1)
    // - saves new likes or deletes for unlikes
    fetch(`/like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            like_count: data,
        }),
    })
}

function follow(username, followed) {

    const follow_button_div = document.getElementById("follow_button_div");
    const button = follow_button_div.querySelector("button");

    // if the account is being unfollowed - (already) followed = true:
    if (followed == true) {
        button.innerHTML = "Follow"
        button.setAttribute("id", "follow_button");
        button.setAttribute("onclick", `follow('${username}', false)`)
        // decrease the follower count
        follower_count.innerHTML--
    }
    // if the account is being followed:
    else {
        button.innerHTML = "Following"
        button.setAttribute("id", "unfollow_button");
        button.setAttribute("onclick", `follow('${username}', true)`)
        follower_count.innerHTML++
    }

    fetch(`/profile/${username}/follow`, {
        method: 'PUT',
    })
}

function change_page(direction) {

    // Get the current page from the URL (default is page = 1)
    let current_page = parseInt(new URLSearchParams(window.location.search).get("page") || 1);

    if (direction == 'next') {
        page = current_page + 1
        link = document.getElementById("next_page_link")
    } else if (current_page > 1) {
        page = current_page - 1
        link = document.getElementById("prev_page_link")
    }

    // Updates the href to the selected link for the new page number
    link.setAttribute("href", `?page=${page}`)
}