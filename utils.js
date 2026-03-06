function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
}

function radiansToDegrees(radians) {
  return radians * (180 / Math.PI);
}

function correctOcrCoordinates(
  ocrYaw,
  ocrPitch,
  streetViewPitch,
  streetViewRoll
) {
  // The original streetview pitch has 90 set as the horizon, so we need to adjust it to 0
  streetViewPitch = 90 - streetViewPitch;

  // Convert degrees to radians
  const ocrYawRad = degreesToRadians(ocrYaw);
  const ocrPitchRad = degreesToRadians(ocrPitch);
  const streetViewPitchRad = degreesToRadians(streetViewPitch);
  const streetViewRollRad = degreesToRadians(streetViewRoll);

  // Calculate corrected yaw
  const x = Math.cos(ocrYawRad) * Math.cos(ocrPitchRad);
  const y = Math.sin(ocrYawRad) * Math.cos(ocrPitchRad);
  const z = Math.sin(ocrPitchRad);

  // Apply roll rotation
  const x2 = x;
  const y2 = y * Math.cos(streetViewRollRad) - z * Math.sin(streetViewRollRad);
  const z2 = y * Math.sin(streetViewRollRad) + z * Math.cos(streetViewRollRad);

  // Apply pitch rotation
  const x3 =
    x2 * Math.cos(streetViewPitchRad) + z2 * Math.sin(streetViewPitchRad);
  const y3 = y2;
  const z3 =
    -x2 * Math.sin(streetViewPitchRad) + z2 * Math.cos(streetViewPitchRad);

  // Calculate corrected yaw and pitch
  const correctedYaw = radiansToDegrees(Math.atan2(y3, x3));
  const correctedPitch = radiansToDegrees(Math.asin(z3));

  return { correctedYaw, correctedPitch };
}

function fovToZoomLevel(fov) {
  if (fov <= 0 || fov >= 180) {
    throw new Error('FOV must be between 0 and 180 degrees');
  }

  const zoomLevel = Math.log2(360 / fov);
  return Math.round(zoomLevel * 100) / 100;
}

class GoogleStreetViewProps {
  constructor(lat, lng, panoramaId, heading, pitch, tilt, fov, zoom) {
    this.lat = lat;
    this.lng = lng;
    this.panoramaId = panoramaId;
    this.heading = heading;
    this.pitch = pitch;
    this.tilt = tilt;
    this.fov = fov;
    this.zoom = zoom;
  }
}

function getGoogleStreetviewProps(
  panoramaId,
  lat,
  lng,
  ocrYaw,
  ocrPitch,
  streetViewHeading,
  streetViewPitch,
  streetViewRoll,
  ocrWidth,
  ocrHeight,
  FOV_FACTOR = 1,
  FOV_MIN = 10
) {
  const { correctedYaw, correctedPitch } = correctOcrCoordinates(
    ocrYaw,
    ocrPitch,
    streetViewPitch,
    streetViewRoll
  );

  const ocrBoundingDegree = Math.ceil(
    Math.max(ocrWidth, ocrHeight) * FOV_FACTOR
  );
  const fov = Math.max(ocrBoundingDegree, FOV_MIN);
  const zoom = fovToZoomLevel(fov);

  return new GoogleStreetViewProps(
    lat,
    lng,
    panoramaId,
    (correctedYaw + streetViewHeading) % 360,
    correctedPitch,
    correctedPitch + 90,
    fov,
    zoom
  );
}

function getGoogleStreetviewUrl(gsvProp) {
  return `https://www.google.com/maps/@${gsvProp.lat},${
    gsvProp.lng
  },3a,20y,${Math.round(gsvProp.heading, 2)}h,${Math.round(
    gsvProp.tilt,
    2
  )}t/data=!3m6!1e1!3m4!1s${gsvProp.panoramaId}!2e0!7i16384!8i8192?entry=ttu`;
}

function getGoogleStreetviewEmbedUrl(gsvProp, GOOGLE_MAPS_API_KEY) {
  if (!GOOGLE_MAPS_API_KEY) {
    throw new Error('GOOGLE_MAPS_API_KEY is required');
  }

  const { lat, lng, panoramaId, heading, pitch, tilt, fov, zoom } = gsvProp;

  const baseURL = 'https://www.google.com/maps/embed/v1/streetview';
  const params = new URLSearchParams();
  params.append('key', GOOGLE_MAPS_API_KEY);
  params.append('location', `${lat},${lng}`);
  params.append('pano', panoramaId);
  params.append('heading', `${heading.toFixed(2)}`);
  params.append('pitch', `${pitch.toFixed(2)}`);
  params.append('fov', `${fov}`);

  const url = `${baseURL}?${params.toString()}`;

  return url;
}
