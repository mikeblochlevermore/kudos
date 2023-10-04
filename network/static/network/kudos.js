document.addEventListener('DOMContentLoaded', function() {

    // By default, load the inbox
    view_posts();
  });


function view_posts() {

    fetch(`/view_posts`)
    .then(response => response.json())
    .then(posts => {

      // Selects the emails-list div newly created above in the #emails-view div
      const postList = document.querySelector('#posts');

      // Loop through each email and create HTML elements
      posts.forEach(post => {

        console.log(post)

          // change the id of the div to #read if the read state is true (changes the styling)
            var element = document.createElement("div");
            element.innerHTML =
                `
                <strong>${post.user}</strong>
                <div>${post.time}</div>
                <div>${post.content}</div>
                </div>
                `;
                postList.append(element);
          })
      });
}