import assert from 'node:assert/strict';
import test from 'node:test';

import {
  hasOAuthScope,
  locationAddressMatches,
  normalizeText,
  selectExpectedLocation,
} from '../scripts/gbp-approval-watch.mjs';

test('requires the Business Profile scope on refreshed owner tokens', () => {
  assert.equal(
    hasOAuthScope(
      'openid https://www.googleapis.com/auth/userinfo.email ' +
        'https://www.googleapis.com/auth/business.manage'
    ),
    true
  );
  assert.equal(hasOAuthScope('openid https://www.googleapis.com/auth/userinfo.email'), false);
});

function candidate(title, name = 'locations/123', account = 'accounts/456') {
  return {
    account,
    location: {
      name,
      title,
      storefrontAddress: {
        addressLines: ['1526 Le Clark Road'],
        locality: 'Carroll',
        administrativeArea: 'IA',
      },
    },
  };
}

test('normalizes Road and Rd for exact address matching', () => {
  assert.equal(normalizeText('1526 Le Clark Road'), '1526 le clark rd');
  assert.equal(locationAddressMatches(candidate('Motor Inn Auto Group').location), true);
});

test('prefers the confirmed combined Carroll profile over the group alias', () => {
  const group = candidate('Motor Inn Auto Group', 'locations/group');
  const combined = candidate(
    'Motor Inn Toyota and Chevrolet of Carroll',
    'locations/combined'
  );
  const result = selectExpectedLocation([group, combined]);
  assert.equal(result.status, 'selected');
  assert.equal(result.candidate.location.name, 'locations/combined');
});

test('rejects a same-name profile at a different address', () => {
  const wrong = candidate('Motor Inn Toyota and Chevrolet of Carroll');
  wrong.location.storefrontAddress.addressLines = ['123 Wrong Rd'];
  const result = selectExpectedLocation([wrong]);
  assert.equal(result.status, 'missing');
});

test('blocks ambiguous duplicate profiles instead of selecting the first', () => {
  const result = selectExpectedLocation([
    candidate('Motor Inn Toyota and Chevrolet of Carroll', 'locations/one'),
    candidate('Motor Inn Toyota and Chevrolet of Carroll', 'locations/two'),
  ]);
  assert.equal(result.status, 'ambiguous');
});
