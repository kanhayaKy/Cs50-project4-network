document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit =  event => send_mail(event);

  window.onpopstate = function(event) {
    //Check if ID exists in the mailbox
    if(event.state.mailbox.split('/')[1]){
      mailbox = event.state.mailbox.split('/')[0];
      id = event.state.mailbox.split('/')[1];
      //fetch the email
      fetch(`/emails/${id}`)
      .then(response => response.json())
      .then(email => {
          view_mail(email,mailbox);
      });
    }
    //load mailbox if id does not exist
    else
      load_mailbox(event.state.mailbox);
}

  document.querySelectorAll(".mailbox-button").forEach(button =>{
    button.onclick = function(){
      const mailbox = this.id;
      history.pushState({mailbox:mailbox},`${mailbox}`,`#${mailbox}`);
    }
  })

  //By default, load the inbox
  history.pushState({mailbox:'inbox'},"",`#inbox`);
  load_mailbox('inbox');
});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


}

function reply_email(email){
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#single-email-view').style.display = 'none';
    document.querySelector('#compose-view-heading').innerHTML = `Reply to ${email.sender}`
    

    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = email.subject.slice(0,3) == "Re:"? email.subject: "Re:"+email.subject;
    document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : "${email.body}"`;


}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  

  // Show the mailbox name
  document.querySelector('#emails-view-name').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load the emails of the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      //Display the emails in the form of list
      emailList = "";
      emails.forEach(mail => {
          emailList += `<div id = "email" class="list-group-item  emailList" data-email-id = "${mail.id}"><h5>${mail.sender}</h5> <p>${mail.subject}</p> <small>${mail.timestamp}</small></div>`;
        });
      document.querySelector("#email-view-emails").innerHTML = emailList;

      //Add event Listener to each email
      emails.forEach(mail => {
        document.querySelector(`[data-email-id= '${mail.id}']`).addEventListener('click', function  handler(){
          mailId = `${mailbox}/${mail.id}`;
          history.pushState({mailbox:mailId,},"",`#${mailId}`);
          view_mail(mail,mailbox);
          this.removeEventListener('click',handler)
        });


        //Check if email is read
        if(mail.read){
          document.querySelector(`[data-email-id= '${mail.id}']`).style.backgroundColor = "#ececec"

        }
      });   
  });
}


function send_mail(event){

  //Make a post request to send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
    //Display errors if any
    if(result.error){
      compose_email()
      alert(`${result.error}`)
    }else{

      document.querySelector(".alert").classList.remove("d-none");
      setTimeout(() => {
        document.querySelector(".alert").classList.add("d-none");

      }, 3000);
      //Load the sent mailbox when email is sent
      history.pushState({mailbox:'sent'},"",`#sent`);
      load_mailbox('sent')
    }
  });

  //Prevent the default submission of from
  return false; 
}


function view_mail(email , mailbox){
  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

    
  //Mark the email read if its not read
  if(!email.read){
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  }

  //Hide the archive button in sent mailbox
  if(mailbox=="sent"){
    document.querySelector("#archive-button").style.display = "none";
  }else{
    document.querySelector("#archive-button").style.display = null;
    //Event listener to archive an email
    e = (event)=> {archive(email,e) };
    document.querySelector("#archive-button").addEventListener('click' , e);
  }

  //Display Unarchive button if mail is archived
  if(email.archived == true ){
    document.querySelector("#archive-button").value = "Unarchive";
  }else{
    document.querySelector("#archive-button").value = "Archive";
  }





  //Display the contents of the Mail
  document.querySelector('#email-sender').innerHTML = `<strong>From:</strong>${email.sender}`;
  document.querySelector('#email-subject').innerHTML = `<strong>Subject:</strong>${email.subject}`;
  document.querySelector('#email-time').innerHTML = `<strong>Timestamp:</strong>${email.timestamp}`;
  document.querySelector('#email-body').textContent = `${email.body}`;
  document.querySelector('#email-receiver').innerHTML = `<strong>To:</strong>${email.recipients.join()}`
  
 

  document.querySelector("#reply").addEventListener('click' , function compose(){
    reply_email(email)
    this.removeEventListener('click',compose)
  });

}


function archive(email,e){
  console.log("archiving",email,e.target)
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  });
  console.log(email)
  document.querySelector("#archive-button").removeEventListener('click' , e);


  setTimeout(function() {
    load_mailbox("inbox");

  }, 100);
}

