/* Single source of editable review data. No credentials belong in this file.
   null means unknown, never zero. All supplied numbers remain placeholders.
   Ratings must retain the platform's scale; Facebook recommendations are not stars.
   Before setting verified:true, check the exact Carroll entity, source and date.
   Links are outbound navigation only; the page fetches no external resources. */
window.REVIEWS_DATA = {
  preview: true, // Set false only after approved deployment and content verification.
  siteUrl: null, // After domain purchase: https://motorinnautogroupreviews.com/
  organization: {
    name: 'Motor Inn Auto Group',
    url: 'https://www.motorinnautogroup.com/',
    address: {streetAddress:'1526 Le Clark Road',addressLocality:'Carroll',addressRegion:'IA',postalCode:'51401',addressCountry:'US'}
  },
  platforms: [
    {id:'google', name:'Google', entity:'Carroll dealership profile pending confirmation',
      profileUrl:null, writeUrl:null,
      lookupUrl:'https://www.google.com/maps/search/?api=1&query=Motor+Inn+Auto+Group+1526+Le+Clark+Road+Carroll+Iowa',
      linkEvidence:'Exact GBP profile and Get more reviews link needed from the owner.',
      verified:false, checkedAt:null, rating:null, count:null, metric:'stars', scale:5,
      note:'Choose the Carroll location that matches your visit.'},
    {id:'facebook', name:'Facebook', entity:'Motor Inn Auto Group',
      profileUrl:'https://www.facebook.com/MotorInnAutoGroup/', writeUrl:'https://www.facebook.com/MotorInnAutoGroup/', lookupUrl:null,
      linkEvidence:'Linked by the official customer-reviews.aspx page; Recommendations availability needs signed-in verification.',
      verified:false, checkedAt:null, rating:null, count:null, metric:'recommendation-percent', scale:100,
      note:'Open the page’s Reviews or Recommendations section. Sign-in may be required.'},
    {id:'dealerrater', name:'DealerRater', entity:'Motor Inn of Carroll, LLC',
      profileUrl:'https://www.dealerrater.com/dealer/Motor-Inn-of-Carroll-LLC-review-16644/',
      writeUrl:'https://www.dealerrater.com/dealer/Motor-Inn-of-Carroll-LLC-review-16644/', lookupUrl:null,
      linkEvidence:'Profile linked from the DealerRater Iowa Toyota directory; direct page retrieval unavailable during build.',
      verified:false, checkedAt:null, rating:null, count:null, metric:'stars', scale:5,
      note:'Use the review option on the dealer profile. A current rating may not be available.'},
    {id:'cars', name:'Cars.com', entity:'Carroll dealership profile pending confirmation',
      profileUrl:null, writeUrl:null, lookupUrl:'https://www.cars.com/dealers/',
      linkEvidence:'Exact Motor Inn Carroll profile was not found in the bounded search. Do not substitute another dealer.',
      verified:false, checkedAt:null, rating:null, count:null, metric:'stars', scale:5,
      note:'Find the Carroll profile before reading or submitting a dealership review.'},
    {id:'cargurus', name:'CarGurus', entity:'Motor Inn of Carroll',
      profileUrl:'https://www.cargurus.com/Cars/m-Motor-Inn-of-Carroll-sp368029',
      writeUrl:'https://www.cargurus.com/Cars/m-Motor-Inn-of-Carroll-sp368029', lookupUrl:null,
      linkEvidence:'Public CarGurus profile retrieved 2026-09-16; no rating/count copied.',
      verified:false, checkedAt:null, rating:null, count:null, metric:'stars', scale:5,
      note:'Follow CarGurus review eligibility and invitation instructions; a review option may require an eligible interaction.'}
  ],
  /* Optional quoted reviews, with permission and provenance. Never invent text.
     Add objects shaped as follows (all fields are required):
     {author:'Public display name', text:'Exact permitted review text',
      date:'YYYY-MM-DD', rating:5, scale:5, sourceUrl:'https://...',
      platformId:'google', verified:true, permissionConfirmed:true,
      origin:'third-party'}
     All valid entries display; do not select only favorable experiences.
     first-party entries use origin:'first-party' and platformId:'first-party'. */
  reviews: [],
  /* Requested AggregateRating/Review support is implemented but disabled.
     Google disallows aggregating other sites' ratings for review rich results;
     a dealer-controlled reviews domain also remains self-serving.
     Do NOT enable for scraped/combined Google/Facebook/DealerRater/Cars/CarGurus scores.
     Optional first-party aggregate must summarize the complete eligible on-site set,
     not just displayed excerpts, and must also appear visibly on the page. */
  structuredReviews: {
    enabled:false,
    aggregate:{verified:false, origin:'first-party', rating:null, count:null, scale:5, checkedAt:null, sourceUrl:null}
  }
};
