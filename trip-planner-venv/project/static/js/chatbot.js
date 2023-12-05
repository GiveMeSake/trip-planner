
"use strict";
(function ($) {
    var container;
    var messageID = 1;
    let answers = [""];
    var delay = 1500;

    function fetchJsonData(callback) {
        $.get("/static/js/questions.json", function(dataJSON) {
            callback(dataJSON);
        });
    }

    $.fn.chunkosChat = function (options) {
        // override options with user preferences
        var settings = $.extend({
            autoStart: true,
            startMessageId: 1,
            dataJSON: null
        }, options);
        container = $(this);

        startChat(container, settings.dataJSON, delay)
    }

    function startChat(container, data, delay) {
        container.html('<div class="chat-inner"></div>');
        var message = findMessageInJsonById(data, messageID);
        generateMessageHTML(container, message,"questions", delay);
        messageID++;
        setTimeout(function() {
            message = findMessageInJsonById(data, messageID);
            generateMessageHTML(container, message, "questions", delay);
        }, delay); 
    }

    function findMessageInJsonById(data, id) {
        var messages = data;
        let msg = messages.filter((el) => {
            return el.id == id
        })[0]
        if (msg) {
            return msg;
        }
    }

    function toggleLoader(status, container) {
        if (status == "show") {
            container.children('.chat-inner').append(`<div class="message-wrapper typing"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`);
        }
        else {
            container.find('.typing').remove();
        }
    }

    function generateMessageHTML(container, message, field, delay) {
        var planner_imageUrl = "/static/images/planner_avatar.gif"
        var $template = $(`<div class="message-wrapper"><div class="chat-bubble left img"><img src="${planner_imageUrl}" alt="" width="60" height="60" class="img-fluid"></div></div>`);
        // console.log(message.questions)
        if (field === 'questions') {
            message?.questions.forEach(el => {
                let $questionElm = $(`<div class="chat-bubble left">${el?.text}</div>`);
                $template.append($questionElm);
            })  
        } else if (field === 'errors') {
            message?.errors.forEach(el => {
                let $errorElm = $(`<div class="chat-bubble left error">${el?.text}</div>`);
                $template.append($errorElm);
            });
        }      
        toggleLoader("show", container);
        container.scrollTop(container.prop('scrollHeight'));
        setTimeout(function () {
            toggleLoader("hide", container);
            container.children('.chat-inner').append($template);
            container.scrollTop(container.prop('scrollHeight'));
        }, delay);
        // end delay
    }

    function processUserMessage(userMessage, isValid, csrfToken) {
        fetchJsonData(function(dataJSON){
            if (isValid == 1){
                messageID++;
                answers.push(userMessage);
                message = findMessageInJsonById(dataJSON, messageID);
                if(message.nextMessageId == "0"){
                    var finalPrompt = message.validationText
                    answers.forEach((answer, index) => {
                        finalPrompt = finalPrompt.replace(`{answers[${index}]}`, answer);
                    });
                    showResultPage(csrfToken, finalPrompt);
                }
                generateMessageHTML(container, message, "questions", delay);
            } else {
                var message = findMessageInJsonById(dataJSON, messageID);
                message.errors[0].text = message.errors[0].text.replace("{input_to_validate}", userMessage);
                // console.log(message.errors[0].text)
                generateMessageHTML(container, message, "errors", delay);
                setTimeout(function () {
                    generateMessageHTML(container, message, "questions", delay);
                }, delay);
            }      
            if(messageID == 4 || messageID == 5) {
                console.log(messageID)
                activateDatepicker();
            }
            else {
                deactivateDatepicker();
            }     
        });

        
    }

    $(function () {
        fetchJsonData(function(dataJSON) {
            $('#chat-app').chunkosChat({
                dataJSON: dataJSON,
            });
        });
    });

    $('#user-input-form').on('submit', function(e) {
        e.preventDefault(); // Prevents the default form submission action
        var userMessage = $('#user-message').val().trim();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        if (userMessage !== '') {
            var user_imageUrl = "/static/images/user_avatar.png"
            var $msgTemplate = $(`<div class="message-wrapper"><div class="chat-bubble right img"><img src="${user_imageUrl}" alt="" width="60" height="60" class="img-fluid"></div></div>`);
            var userMessageHTML = `<div class="chat-bubble right">${userMessage}</div>`;
            $('#user-message').val(''); // Clear the input field after sending the message
            $msgTemplate.append(userMessageHTML);
            container.children('.chat-inner').append($msgTemplate);
            fetchJsonData(function(dataJSON){
                var message = findMessageInJsonById(dataJSON, messageID);
                message.validationText = message.validationText.replace("{input_to_validate}", userMessage);
                    validateUserInput(csrfToken, "Location", message.validationText, function(isValid) {
                        processUserMessage(userMessage, isValid, csrfToken);
                    });           
            });
            
        }
    });

    function showResultPage(csrfToken, finalPrompt){
        // console.log(finalPrompt)
        $.ajax({
            type: 'POST',
            url: '/show_results/', // URL to the Django view
            data: {
                'finalPrompt': finalPrompt,
                'csrfmiddlewaretoken': csrfToken // CSRF token
            },
            success: function(response) {
                document.documentElement.innerHTML = response;
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }
    
    function validateUserInput(csrfToken, field, validationText, callback) {
        $.ajax({
            type: 'POST',
            url: '/input_validation/', // URL to the Django view
            data: {
                'validation_field' : field,
                'validationText': validationText,
                'csrfmiddlewaretoken': csrfToken // CSRF token
            },
            success: function(response) {
                callback(response.isValid);
            },
            error: function(error) {
                console.log('Error:', error);
                callback(false);
            }
        });
    }

    function initializeDatepicker() {
        $("#user-message").datepicker();
    }

    function activateDatepicker() {
        if (!$('#user-message').hasClass('hasDatepicker')) {
            $("#user-message").datepicker();
        }
    }

    function deactivateDatepicker() {
        $("#user-message").datepicker('destroy');
    }

    function isValidDateFormat(dateString) {
        // Regular expression for the date format MM/DD/YYYY
        const regex = /^(0[1-9]|1[0-2])\/(0[1-9]|[12][0-9]|3[01])\/\d{4}$/;

        // Test the date string against the regular expression
        if (regex.test(dateString)) {
            // Further check to ensure the date is valid (e.g., not February 30th)
            const parts = dateString.split('/');
            const month = parseInt(parts[0], 10);
            const day = parseInt(parts[1], 10);
            const year = parseInt(parts[2], 10);
            
            if (regex.test(dateString))
                return 1;
            } else {
                // Date does not match format
                return 0;
            }
        }

}(jQuery));