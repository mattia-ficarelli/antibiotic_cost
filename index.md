<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

## The Prescribing Cost of Antibiotics

[Antibiotics](https://www.nhs.uk/conditions/antibiotics/) are used to treat or prevent bacterial infections. There are many different types of antibiotics and some of the most prescribed include:

  - [Amoxicillin](https://www.nhs.uk/medicines/amoxicillin/), used to treat skin infections, chest infections and urinary tract infections.
  - [Doxycycline Hyclate](https://www.nhs.uk/medicines/doxycycline/), used to treat a skin condition called rosacea, dental infections, and sexually transmitted infections (STIs).
  - [Cefalexin](https://www.nhs.uk/medicines/cefalexin/), used to treat pneumonia and other chest infections.

The overuse of antibiotics has led to the emergence of [antibiotic-resistant bacteria](https://www.nhs.uk/conditions/antibiotics/antibiotic-antimicrobial-resistance/), which cause infections that can be serious and challenging to treat as they no longer respond to many types of existing antibiotics. Antibiotic resistance is viewed as a critical public health challenge, with the NHS and health organisations across the world trying to reduce the use of antibiotics to combat rising antimicrobial resistance rates. 

This page tracks the prescribing cost of certain antibiotic types over time and by [Clinical Commissioning Groups (CCGs)](https://www.england.nhs.uk/ccgs/).

Data sources: [NHS Digital](https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice) and [OpenPrescribing.net](https://openprescribing.net/).

<hr class="nhsuk-u-margin-top-0 nhsuk-u-margin-bottom-6">

{% include update.html %}

### Prescribing cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per month 

{% include plotly_obj.html %}

<div class="nhsuk-action-link">
  <a class="nhsuk-action-link__link" href="assets/data/cost_antibiotics_per_month.csv">
    <svg class="nhsuk-icon nhsuk-icon__arrow-right-circle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M0 0h24v24H0z" fill="none"></path>
      <path d="M12 2a10 10 0 0 0-9.95 9h11.64L9.74 7.05a1 1 0 0 1 1.41-1.41l5.66 5.65a1 1 0 0 1 0 1.42l-5.66 5.65a1 1 0 0 1-1.41 0 1 1 0 0 1 0-1.41L13.69 13H2.05A10 10 0 1 0 12 2z"></path>
    </svg>
    <span class="nhsuk-action-link__text">Download this dataset (.csv)</span>
  </a>
</div>

### Prescribing cost (£) of Amoxicillin, Doxycycline Hyclate, and Cefalexin per 1000 GP registered population for the current year

<iframe width= "900" height="700"  src="assets/folium/folium_obj.html" style="border:none;"></iframe>

<div class="nhsuk-action-link">
  <a class="nhsuk-action-link__link" href="assets/data/cost_antibiotics_ccg_current_year.csv">
    <svg class="nhsuk-icon nhsuk-icon__arrow-right-circle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M0 0h24v24H0z" fill="none"></path>
      <path d="M12 2a10 10 0 0 0-9.95 9h11.64L9.74 7.05a1 1 0 0 1 1.41-1.41l5.66 5.65a1 1 0 0 1 0 1.42l-5.66 5.65a1 1 0 0 1-1.41 0 1 1 0 0 1 0-1.41L13.69 13H2.05A10 10 0 1 0 12 2z"></path>
    </svg>
    <span class="nhsuk-action-link__text">Download this dataset (.csv)</span>
  </a>
</div>


## About this page

This page is built using end-to-end open source analytical tools including: [The NHS Digital Service Manual](https://service-manual.nhs.uk/), [python](https://nhs-pycom.net/), [plotly](https://plotly.com/python/), [folium](http://python-visualization.github.io/folium/), [github.io](https://pages.github.com/), and [github actions](https://github.com/features/actions).

<div class="nhsuk-action-link">
  <a class="nhsuk-action-link__link" href="https://github.com/nhsx/open-analytics-template">
    <svg class="nhsuk-icon nhsuk-icon__arrow-right-circle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M0 0h24v24H0z" fill="none"></path>
      <path d="M12 2a10 10 0 0 0-9.95 9h11.64L9.74 7.05a1 1 0 0 1 1.41-1.41l5.66 5.65a1 1 0 0 1 0 1.42l-5.66 5.65a1 1 0 0 1-1.41 0 1 1 0 0 1 0-1.41L13.69 13H2.05A10 10 0 1 0 12 2z"></path>
    </svg>
    <span class="nhsuk-action-link__text">Find out how to build your own open analytics pipeline</span>
  </a>
</div>

If you have any suggestions or questions, email: <a href="mailto:mattia.ficarelli@nhsx.nhs.uk">mattia.ficarelli@nhsx.nhs.uk</a>
