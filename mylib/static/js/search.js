// fetch JSON from Google Books API
async function grabVolumeInfo (volumeID) {
    let promise =  await fetch('https://www.googleapis.com/books/v1/volumes/' + volumeID);
      return promise.json()
    }

    // Grab volume ID from search results list to populate record details pane
    let title_links = document.querySelectorAll('tr');
    for (let i = 0; i < title_links.length; i++) {
      title_links[i].addEventListener('click', () => {
        let volumeID = title_links[i].getAttribute("data-record-id");
        let volume = grabVolumeInfo(volumeID)
          .then(volume => {
            let add_btn = document.getElementById('add-btn');
             let description_label = document.getElementById('description-label');

            // change elements in DOM. Title, Subtitle, Publisher, etc...
            add_btn.removeAttribute('style');
            description_label.removeAttribute('style');
            // Check if volume has cover link
            try {
              document.getElementById('cover').setAttribute('src', volume.volumeInfo.imageLinks.thumbnail)
            } catch {
              document.getElementById('cover').setAttribute('src', '/static/assests/blank-cover.svg')
            }

            document.getElementById('title').innerHTML = '<b>Title: </b>' + volume.volumeInfo.title;
            // Check if volume has subtitle
            try {
              document.getElementById('subtitle').innerHTML = '<b>Subtitle: </b>' + volume.volumeInfo.subtitle;
            } catch {
              document.getElementById('subtitle').innerHTML = 'Caught!'
            }
            document.getElementById('authors').innerHTML = '<b>Author(s): </b>' + volume.volumeInfo.authors.join(", ");
            document.getElementById('publisher').innerHTML = '<b>Publisher: </b>' + volume.volumeInfo.publisher;
            document.getElementById('publicationDate').innerHTML = '<b>Publication Date: </b>' + volume.volumeInfo.publishedDate;
            document.getElementById('ISBN').innerHTML = '<b>ISBN: </b>' + volume.volumeInfo.industryIdentifiers[0].identifier;
            document.getElementById('description').innerHTML = volume.volumeInfo.description;
            document.getElementById('add-to-catalog').setAttribute('value', volumeID)
          })
      });
    }