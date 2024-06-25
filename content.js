// New profile picture URL
const newProfilePictureUrl = 'https://i.pinimg.com/736x/9d/da/e1/9ddae18a4909205f52a31586a5435442.jpg';

// Function to replace profile pictures
function replaceProfilePictures() {
    // Targetting profile pictures
    const profilePictures = document.querySelectorAll('img[src*="profile"]');

    profilePictures.forEach((picture) => {
        picture.src = newProfilePictureUrl;
    });
}
// Runs the function on loading the page
window.addEventListener('load', replaceProfilePictures);

// Runs the function on any future DOM updates (as LinkedIn uses dynamic loading)
const observer = new MutationObserver(replaceProfilePictures);
observer.observe(document.body, { childList: true, subtree: true });


