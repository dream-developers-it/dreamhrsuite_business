# Create vendor directories
$vendorPath = "static/iLanding/vendor"
@(
    "bootstrap",
    "bootstrap/css",
    "bootstrap/js",
    "bootstrap-icons",
    "bootstrap-icons/fonts",
    "aos",
    "aos/css",
    "aos/js",
    "glightbox",
    "glightbox/css",
    "glightbox/js",
    "swiper",
    "swiper/css",
    "swiper/js"
) | ForEach-Object {
    New-Item -ItemType Directory -Force -Path "$vendorPath/$_" | Out-Null
}

# Function to download file
function Download-File {
    param(
        [string]$Url,
        [string]$OutFile
    )
    Write-Host "Downloading $Url to $OutFile"
    Invoke-WebRequest -Uri $Url -OutFile $OutFile
}

# Bootstrap
Download-File "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" "$vendorPath/bootstrap/css/bootstrap.min.css"
Download-File "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" "$vendorPath/bootstrap/js/bootstrap.bundle.min.js"

# Bootstrap Icons
Download-File "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" "$vendorPath/bootstrap-icons/bootstrap-icons.css"
Download-File "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff" "$vendorPath/bootstrap-icons/fonts/bootstrap-icons.woff"
Download-File "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/fonts/bootstrap-icons.woff2" "$vendorPath/bootstrap-icons/fonts/bootstrap-icons.woff2"

# AOS (Animate On Scroll)
Download-File "https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" "$vendorPath/aos/css/aos.css"
Download-File "https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js" "$vendorPath/aos/js/aos.js"

# GLightbox
Download-File "https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/css/glightbox.min.css" "$vendorPath/glightbox/css/glightbox.min.css"
Download-File "https://cdn.jsdelivr.net/npm/glightbox@3.2.0/dist/js/glightbox.min.js" "$vendorPath/glightbox/js/glightbox.min.js"

# Swiper
Download-File "https://cdn.jsdelivr.net/npm/swiper@11.0.5/swiper-bundle.min.css" "$vendorPath/swiper/css/swiper-bundle.min.css"
Download-File "https://cdn.jsdelivr.net/npm/swiper@11.0.5/swiper-bundle.min.js" "$vendorPath/swiper/js/swiper-bundle.min.js"

# Create img directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "static/iLanding/img" | Out-Null

# Download sample images
$images = @{
    "hero-img.svg" = "https://raw.githubusercontent.com/bootstrapmade/iLanding/master/assets/img/hero-img.svg"
    "about.jpg" = "https://raw.githubusercontent.com/bootstrapmade/iLanding/master/assets/img/about.jpg"
    "favicon.png" = "https://raw.githubusercontent.com/bootstrapmade/iLanding/master/assets/img/favicon.png"
    "apple-touch-icon.png" = "https://raw.githubusercontent.com/bootstrapmade/iLanding/master/assets/img/apple-touch-icon.png"
    "logo.png" = "https://raw.githubusercontent.com/bootstrapmade/iLanding/master/assets/img/logo.png"
}

foreach ($image in $images.GetEnumerator()) {
    Download-File $image.Value "static/iLanding/img/$($image.Name)"
}

Write-Host "All assets have been downloaded successfully!"
