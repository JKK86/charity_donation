document.addEventListener("DOMContentLoaded", function () {
    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;
            // fetch('/' + `?page=${page}`)
            //     .then(res => res.json())

            console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
            const categories = document.querySelectorAll("input[name='categories']");
            const bags = document.querySelector("input[name='bags']");
            const organization = document.querySelector("input[name='organization']:checked");
            const address = document.querySelector("input[name='address']");
            const city = document.querySelector("input[name='city']");
            const postcode = document.querySelector("input[name='postcode']");
            const phone = document.querySelector("input[name='phone']");
            const date = document.querySelector("input[name='data']");
            const time = document.querySelector("input[name='time']");
            const more_info = document.querySelector("textarea[name='more_info']");

            const summary_bags = document.querySelector("#summary-bags");
            const summary_organization = document.querySelector("#summary-organization");
            const summary_address = document.querySelector("#summary-address");
            const summary_date = document.querySelector("#summary-date");

            const next = document.querySelector("div[data-step='4'] button.next-step");

            next.addEventListener('click', evt => {
                const category_names = [];
                categories.forEach(el => {
                    if (el.checked) {
                        category_names.push(el.dataset.category)
                    }
                })
                summary_bags.innerText = `Liczba worków: ${bags.value}; Zawartość: ${category_names.join(', ').toLowerCase()}`;
                summary_organization.innerText = `Dla: ${organization.dataset.institution}`;
                summary_address.firstElementChild.innerText = `${address.value}`;
                summary_address.children[1].innerText = `${city.value}`;
                summary_address.children[2].innerText = `${postcode.value}`;
                summary_address.lastElementChild.innerText = `tel. ${phone.value}`;
                summary_date.firstElementChild.innerText = `${date.value.toString()}`;
                summary_date.children[1].innerText = `g. ${time.value.toString()}`;
                summary_date.lastElementChild.innerText = `Uwagi dla kuriera: 
                ${more_info.value}`;
            })
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});

/**
 * Filter categories in form step 3
 */


const div_step3 = document.querySelectorAll("div[data-step='3'] div.form-group--checkbox");
const checked_categories = document.querySelectorAll("div[data-step='1'] input");
const next = document.querySelector("div[data-step='1'] button.next-step");


next.addEventListener('click', evt => {
    checked_categories.forEach(category => {
    if (category.checked) {
        // console.log(category.value)
        div_step3.forEach(el => {
            // console.log(category.value, el.firstElementChild.lastElementChild.innerText)
            if (!(`category${category.value}` in el.dataset)) {
                el.style.display = 'none';
            }
        })
    }
})

})


// checked_categories.forEach(el => {
//     el.addEventListener('change', evt => {
//         console.log(el.value)
//     })
//
// })

// checked_categories.forEach(category => {
//     if (category.checked) {
//         div_step3.forEach(el => {
//             // console.log(category.value, el.firstElementChild.lastElementChild.innerText)
//             // if (!(el.dataset.category - `${category.value}`)) {
//                 el.style.display = 'none';
//             // }
//         })
//     }
// })



