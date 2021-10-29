var url =
  "https://www.recreation.gov/api/search?fq=campsite_type_of_use%3AOvernight&fq=campsite_type_of_use%3Ana&fq=entity_type%3Acampground&fq=campsite_type_of_use%3ADay&fq=entity_type%3Acampground&sort=distance&start=0&size=19&lat=39.1256&lng=-84.5127&location=Cincinnati%2C%20Ohio&radius=300";

var xhr = new XMLHttpRequest();
xhr.open("GET", url);

xhr.setRequestHeader("authority", "www.recreation.gov");
xhr.setRequestHeader("pragma", "no-cache");
xhr.setRequestHeader("accept", "application/json, text/plain, */*");
xhr.setRequestHeader("cache-control", "no-cache, no-store, must-revalidate");
xhr.setRequestHeader("sec-ch-ua-mobile", "?0");
xhr.setRequestHeader(
  "user-agent",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
);
xhr.setRequestHeader(
  "sec-ch-ua",
  '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"'
);
xhr.setRequestHeader("sec-ch-ua-platform", '"macOS"');
xhr.setRequestHeader("sec-fetch-site", "same-origin");
xhr.setRequestHeader("sec-fetch-mode", "cors");
xhr.setRequestHeader("sec-fetch-dest", "empty");
xhr.setRequestHeader("referer", "https://www.recreation.gov/");
xhr.setRequestHeader("accept-language", "en-US,en;q=0.9");
xhr.setRequestHeader(
  "cookie",
  "_ga=GA1.2.55312094.1630264240; _hjid=70f4dbbf-7af7-43a6-a30e-9a854fbff6fe"
);

xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {
    console.log(xhr.status);
    console.log(xhr.responseText);
  }
};

xhr.send();
