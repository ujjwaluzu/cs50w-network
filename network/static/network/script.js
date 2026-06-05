document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".like-btn").forEach(button => {

        button.addEventListener("click", () => {

            const postId = button.dataset.postId;

            fetch(`/post/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => response.json())
            .then(data => {

                document.querySelector(
                    `#likes-count-${postId}`
                ).innerHTML = `❤️ ${data.likes_count}`;

                button.innerText = data.liked
                    ? "Unlike"
                    : "Like";
            })
            .catch(error => {
                console.error("Error:", error);
            });

        });

    });

});


function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {

            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

                break;
            }
        }
    }

    return cookieValue;
}


const followBtn = document.querySelector("#follow-btn");

if (followBtn) {

    followBtn.addEventListener("click", () => {

        const username = followBtn.dataset.username;

        fetch(`/profile/${username}/follow`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            }
        })
        .then(response => response.json())
        .then(data => {

            document.querySelector("#followers-count")
                .innerText = `Followers: ${data.followers_count}`;

            followBtn.innerText = data.following
                ? "Unfollow"
                : "Follow";
        });

    });

}

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".edit-btn").forEach(button => {

        button.addEventListener("click", () => {

            const postId = button.dataset.postId;

            const titleDiv = document.querySelector(
                `#title-${postId}`
            );

            const contentDiv = document.querySelector(
                `#content-${postId}`
            );

            const currentTitle = titleDiv.innerText;
            const currentContent = contentDiv.innerText;

            titleDiv.innerHTML = `
                <input
                    type="text"
                    class="edit-input"
                    id="edit-title-${postId}"
                    value="${currentTitle}"
                >
            `;

            contentDiv.innerHTML = `
                <textarea
                    class="edit-textarea"
                    id="edit-content-${postId}"
                >${currentContent}</textarea>

                <div class="edit-actions">

                    <button
                        type="button"
                        class="btn btn-success btn-sm save-btn"
                        id="save-${postId}"
                    >
                        Save
                    </button>

                    <button
                        type="button"
                        class="btn btn-danger btn-sm cancel-btn"
                        id="cancel-${postId}"
                    >
                        Cancel
                    </button>

                </div>
            `;

            button.style.display = "none";

            document
                .querySelector(`#save-${postId}`)
                .addEventListener("click", () => {

                    const newTitle =
                        document.querySelector(
                            `#edit-title-${postId}`
                        ).value;

                    const newContent =
                        document.querySelector(
                            `#edit-content-${postId}`
                        ).value;

                    fetch(`/posts/${postId}/edit_ajax`, {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken":
                                getCookie("csrftoken")
                        },

                        body: JSON.stringify({
                            title: newTitle,
                            content: newContent
                        })
                    })
                    .then(response => response.json())
                    .then(data => {

                        titleDiv.innerHTML =
                            data.title;

                        contentDiv.innerHTML =
                            data.content;

                        button.style.display =
                            "inline-block";

                    });

                });

            document
                .querySelector(`#cancel-${postId}`)
                .addEventListener("click", () => {

                    titleDiv.innerHTML =
                        currentTitle;

                    contentDiv.innerHTML =
                        currentContent;

                    button.style.display =
                        "inline-block";

                });

        });

    });

});