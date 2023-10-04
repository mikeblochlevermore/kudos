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
                <strong>${post.user}</strong>
                <div>${post.time}</div>
                <div>${post.content}</div>
                <p id="like_count_${post.id}">${post.like_count}</p>
                </div>
                <button onclick="like(${post.id})" id="like_button_${post.id}">🤍</button>
                `;
                postList.append(element);
          })
      });
}

function like(post_id) {
    console.log("liked", {post_id})

    // updates the like count on the page
    counter = document.getElementById(`like_count_${post_id}`).innerHTML
    counter++
    document.getElementById(`like_count_${post_id}`).innerHTML = counter;

    // Change like button to green
    button = document.getElementById(`like_button_${post_id}`)
    console.log(button)
    button.innerHTML = "💚"

    // sends a PUT request to the API to add the like to the database
    fetch(`/like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          like_count: 1,
        }),
      })
}