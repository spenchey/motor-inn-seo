"""Explicit phrasing source for every H2 and FAQ question.

Value = the real GSC query (from ads/gsc-keywords-12mo.json) whose wording the question follows,
or None = DERIVED: a conversion or support question answered from owner-verified facts. These have
no direct GSC row with 10+ impressions.
"""
D = None

SRC = {
    # contactus-carroll
    "Which car dealerships are in Carroll, Iowa?": "car dealerships carroll iowa",
    "What can I buy at a Carroll car dealership?": "carroll car dealership",
    "Is there a Chevy dealer and a Toyota dealer in Carroll, Iowa?": "carroll iowa chevy dealers",
    "Can I trade in and finance at the same dealership?": D,
    "Can I get my car serviced at a Carroll dealership?": D,
    "How do I schedule a test drive in Carroll?": "schedule a test drive",
    "Where is the car dealership in Carroll, IA?": "car dealership carroll iowa",
    "Can I trade in my car at a Carroll dealership without an appointment?": D,
    "Can I get car financing at a dealership in Carroll, Iowa?": "auto finance carroll ia",
    # used-cars-carroll-iowa
    "Where can I find used cars for sale in Carroll, Iowa?": "used cars for sale carroll ia",
    "Can I find a used car under $20,000 in Carroll?": D,
    "Which used car dealers in Carroll, IA also service what they sell?": "used car dealers carroll ia",
    "Can I trade in my car toward a used car?": D,
    "Can I get financing on a used car in Carroll?": D,
    "Can I test drive a used car before I buy?": "test drive used car",
    "Does a Carroll used car dealer take trade-ins without an appointment?": D,
    "Can I get financing on a used car in Carroll, Iowa?": D,
    "How do I find a used car under $20,000 in Carroll?": D,
    "Are there used car dealerships in Carroll, IA?": "used car dealerships carroll ia",
    # chevy-dealer-carroll-iowa
    "Where is the Chevy dealer in Carroll, Iowa?": "chevy dealer carroll iowa",
    "Is Motor Inn of Carroll a Chevrolet dealer?": "motor inn of carroll l.l.c. chevrolet",
    "Which new Chevrolet models can I shop in Carroll?": "chevrolet carroll iowa",
    "Does the Chevy dealer in Carroll service Chevrolets?": D,
    "Can I trade in or sell my car at the Carroll Chevy dealer?": D,
    "Can I get Chevy financing in Carroll?": D,
    "Is there a Chevy dealer near me?": "chevy dealer near me",
    "Does the Chevy dealer in Carroll, Iowa, do Chevrolet service?": D,
    "Can I trade in my car at the Carroll Chevy dealer without an appointment?": D,
    "Is there a Chevy dealer and a Toyota dealer at the same place in Carroll?": "motor inn toyota and chevrolet of carroll",
    # chevy-suvs
    "Which Chevy SUVs can I buy near me in Carroll?": "chevy suv near me",
    "Which Chevy SUV is best for families?": "best chevy suv for families",
    "Where can I find a Chevy Suburban in Carroll, Iowa?": "carroll iowa chevy suburban",
    "How do I get Chevy SUV lease deals near me?": "equinox lease near me",
    "Can I buy a used Chevy SUV in Carroll?": D,
    "Where can I buy a Chevy SUV in Carroll, Iowa?": "chevy suv for sale",
    "What is the best Chevy SUV for families?": "best chevy suv for families",
    "How do I find Chevy Equinox or Tahoe lease deals near Carroll?": "tahoe deals near me",
    # chevy-blazer
    "Where can I find a Chevy Blazer for sale near me?": "chevy blazer for sale near me",
    "What's the difference between the Blazer and the Blazer EV?": "chevy blazer ev near me",
    "How do I get Chevy Blazer lease prices near me?": "chevy blazer lease prices near me",
    "Can I test drive a Blazer in Carroll?": D,
    "Can I trade in my car toward a Blazer?": D,
    "Where can I find a Chevy Blazer for sale near Carroll, Iowa?": "chevy blazers for sale near me",
    "What is the difference between the Chevy Blazer and the Blazer EV?": "chevy blazer ev near me",
    "Can I test drive a Chevy Blazer in Carroll, Iowa?": D,
    # chevy-trucks
    "Where can I find a Chevy truck for sale near me?": "chevy truck for sale near me",
    "Which Chevy truck should I buy?": "chevy trucks",
    "Is a Chevy 2500 for sale in Carroll?": "chevy 2500 for sale",
    "How do I get Silverado lease deals near me?": "silverado lease deals near me",
    "Can I buy a used Chevy Silverado or Colorado in Carroll?": D,  # support section; used intent routes to group /used-trucks
    "Where can I find a Chevy truck for sale near Carroll, Iowa?": "chevrolet truck for sale",
    "Is a Chevy 2500 for sale in Carroll, Iowa?": "chevrolet 2500 for sale",
        # toyota-dealers-in-iowa
    "Where are Toyota dealers in Iowa?": "toyota dealers in iowa",
    "Is there a Toyota dealership near me?": "toyota dealership near me",
    "What can I buy at a Toyota dealer in Carroll, Iowa?": "toyota dealer carroll iowa",
    "Where can I get Toyota service near me?": "toyota service near me",
    "Can I trade in and finance at the Carroll Toyota dealer?": D,
    "Where is a Toyota dealer in west-central Iowa?": "toyota dealer in iowa",
    "Is there a Toyota dealership in Carroll, Iowa?": "toyota dealership carroll iowa",
    "Where can I get Toyota service near Carroll, Iowa?": "toyota service",
    "Does Motor Inn Toyota of Carroll sell Certified Pre-Owned Toyotas?": "toyota used cars near me",
    "Can I trade in my car at the Toyota dealer in Carroll without an appointment?": D,
    # toyota-tacoma-tundra
    "Where can I find a Toyota Tacoma for sale near me?": "toyota tacoma for sale near me",
    "Is a Toyota Tundra for sale in Carroll?": "toyota tundra for sale",
    "Tacoma or Tundra: which Toyota truck fits?": D,
    "Can I buy a used Toyota Tacoma?": D,  # support section; used intent routes to group
    "Can I trade in and finance a Toyota truck in Carroll?": D,
    "Where can I find a Toyota Tacoma for sale near Carroll, Iowa?": "toyota tacoma for sale",
    "Is a Toyota Tundra for sale in Carroll, Iowa?": "toyota tundra for sale trd pro",
    "What is the difference between the Toyota Tacoma and Tundra?": D,
        # toyota-sequoia-sienna
    "Where can I find a Toyota Sequoia for sale near me?": "toyota sequoia for sale near me",
    "Is a Toyota Sienna for sale near Carroll?": "toyota sienna for sale",
    "Sequoia or Sienna: which fits your family?": D,
    "What Toyota is bigger than a Highlander?": "what toyota is bigger than a highlander",
    "Can I buy a used Sequoia or Sienna in Carroll?": D,
    "Where can I find a Toyota Sequoia for sale near Carroll, Iowa?": "toyota sequoia for sale",
    "Is a Toyota Sienna for sale in Carroll, Iowa?": "toyota sienna for sale",
    "Should I buy a Toyota Sequoia or a Toyota Sienna?": D,
}
