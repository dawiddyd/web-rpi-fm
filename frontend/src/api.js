import axios from 'axios';

export const api = {
   error: null,
   loading: false,
   songs: [],
   now_playing: require('./assets/cover2.jpg'),


async getLs() {
  var songs = (await axios.get(`/ls`)).data;
  return songs;
},


async uploadFile(formData) {
    try {
        this.clearError();
        await axios.post(`/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.setSuccess("", "Pomyślnie zmieniono avatar");
      } catch (e) {
        this.processException(e);
      }
},

   processException(e) {
     if (typeof (e) == "string")
       this.setError(e);
     else {
       if (e.response && e.response.data && e.response.data.message)
         this.setError(e.response.data.title, e.response.data.message);
       else if (e.response && e.response.status)
         this.setError(`Nieznany błąd ${e.response.status}`, e);
       else
         this.setError("Nieznany błąd", e.toString());
     }
   },

   setError(title, body) {
     if (!body)
       this.error = {
         title: "Wystąpił błąd",
         body: title,
         isError: true,
       };
     else
       this.error = {
         title: title,
         body: body,
         isError: true,
       };
   },

   setSuccess(title, body) {
     if (!body)
       this.error = {
         title: "Sukces!",
         body: title,
         isError: false,
       };
     else
       this.error = {
         title: title,
         body: body,
         isError: false,
       };
   },

   clearError() {
     this.error = null;
   }


}