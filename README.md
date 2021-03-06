# CONCERT TALENT
### a contact and reputation manager for musicians and contractors.

## ABOUT THE APP

Concert Talent is like LinkedIn meets Klout for freelance musicians and the people who hire them.  

More than merely another platform for garage bands and/or singer-songwriters to promote themselves via assorted media embeds and self-aggrandizing profile blurbs, Concert Talent aims to serve the unique needs of industry professionals who manage studio, session, and touring players--i.e., artists who customarily work at a relatively high level in the industry and in ad-hoc ensembles assembled for a specific purpose. 

The app includes features that facilitate the work of managing executives and ensemble leaders who hire for: TV and film scoring sessions (a global industry--Los Angeles, Seattle, London, Prague and elsewhere); productions touring worldwide for major label headlining artists and Broadway shows; local presenters of any sort of concert series; labels and producers organizing local recording dates, and more.  

The app is presently in a pre-release alpha mode / test phase, and several features are planned for development pending further market validation and additional traction from early adopters.

------------------------------------------------------------------------

## TECHNOLOGY STACK

Right now, the app is a lightweight landing page with mobile-friendly and responsive styling via a Bootstrap theme. The page is served up via Flask (i.e., Python) + uWSGI + Nginx deployed on Ubuntu Server 12.04.1 LTS and hosted on an Amazon EC2 instance. Static files are stored on Amazon S3, and pushed through Amazon's CloudFront CDN; DNS routing is managed by Amazon's Route53. A load balancer sits in front of the application server, and can easily be connected to additional application servers in the event growing traffic warrants it.

------------------------------------------------------------------------

## LICENSE

At this time, since the app is merely a standard Flask deployment on EC2, the code is available via the MIT license.  

However, please note, the Concert Talent name and logo, all original artwork, and original written copy pertaining specifically to Concert Talent are proprietary and may not be duplicated.  However, at this time, you are free to clone this repo and refactor the code therein and incorporate your own styling to generate another website with similar functionality.  Please do not replicate any proprietary styling or brand related features--i.e., visual or written elements--of the Concert Talent website on your own URL without the express written permission to do so.  Attribution / credit is appreciated but not required.

------------------------------------------------------------------------

## TO DO

This is a pre-alpha release.  Additional Facebook integration, user authentication / authorization, and profiles incorporating geo-location data in preparaton for an ensemble builder widget are in development.

------------------------------------------------------------------------

## CONTACT

You can keep up to date with release info via http://facebook.com/concerttalent, or by registering at http://concerttalent.com.

Your input is highly valued. Feel free to e-mail me directly and make suggestions or ask questions.  You can reach me via sean@blogblimp.com




