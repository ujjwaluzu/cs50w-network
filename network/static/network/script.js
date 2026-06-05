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