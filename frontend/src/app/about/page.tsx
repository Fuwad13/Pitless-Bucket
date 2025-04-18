import React from "react";

import {
  Cloud,
  Shuffle,
  Sparkles,
  Link2,
  Combine,
  UploadCloud,
  DownloadCloud,
  Settings2,
} from "lucide-react";

const About: React.FC = () => {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <main className="flex-1 p-6 md:p-8 lg:p-10 overflow-y-auto">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12 md:mb-16">
            <Cloud className="inline-block h-10 w-10 text-blue-500 mb-2" />{" "}
            <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 mb-4">
              Welcome to Pitless Bucket!
            </h1>
            <p className="text-lg md:text-xl text-gray-600 leading-relaxed max-w-3xl mx-auto">
              Your scattered cloud files have found their new, unified home.
              Let&apos;s simplify your digital life, together.
            </p>
          </div>

          <section className="mb-12 md:mb-16 p-6 bg-white rounded-xl shadow-lg border border-gray-100">
            <div className="flex items-center gap-3 mb-4 text-center">
              {/* <Shuffle className="h-8 w-8 text-red-500 " /> */}
              <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 mx-auto">
                Sound Familiar? The Cloud Chaos
              </h2>
            </div>
            <p className="text-gray-700 leading-relaxed text-base md:text-lg text-center">
              Juggling multiple Google Drives for work and personal stuff? Throw
              Dropbox into the mix? 🤯 Remembering where that <b>one</b> file
              is, constantly logging in and out, trying to move things between
              services... it&apos;s a time-sink and a headache we know all too
              well.
            </p>
          </section>

          <section className="mb-12 md:mb-16 p-6 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl shadow-xl">
            {" "}
            <div className="flex items-center gap-3 mb-4">
              <Sparkles className="h-8 w-8 text-yellow-300" />{" "}
              <h2 className="text-2xl md:text-3xl font-semibold">
                ✨ Enter Pitless Bucket: Your Cloud Control Center
              </h2>
            </div>
            <p className="text-blue-100 leading-relaxed mb-6 text-base md:text-lg text-center">
              We built Pitlessbucket to cut through the clutter. It&apos;s your
              single, secure dashboard to wrangle all those scattered files:
            </p>
            <ul className="space-y-4">
              {[
                {
                  icon: Link2,
                  title: "Connect Multiple Accounts",
                  description:
                    "Securely link various Google Drive and Dropbox accounts. More coming soon!",
                  color: "text-green-300",
                },
                {
                  icon: Combine,
                  title: "Aggregate Everything",
                  description:
                    "See files and folders from *all* connected accounts right here. No more hunting!",
                  color: "text-purple-300",
                },
                // {
                //   icon: UploadCloud,
                //   title: "Upload Anywhere",
                //   description:
                //     "Choose exactly which cloud account gets your new files, directly from Pitlessbucket.",
                //   color: "text-orange-300",
                // },
                {
                  icon: DownloadCloud,
                  title: "Download with Ease",
                  description:
                    "Grab any file you need, no matter which connected cloud drive it lives on.",
                  color: "text-cyan-300",
                },
                {
                  icon: Settings2,
                  title: "Centralized Management",
                  description:
                    "Browse, access, and organize your cloud data without the usual tab-switching chaos.",
                  color: "text-pink-300",
                },
              ].map((item, index) => (
                <li
                  key={index}
                  className="flex items-start gap-4 p-3 bg-white/10 rounded-lg"
                >
                  <item.icon
                    className={`h-6 w-6 mt-1 flex-shrink-0 ${item.color}`}
                  />

                  <div>
                    <strong className="font-medium text-lg text-white block">
                      {item.title}
                    </strong>
                    <span className="text-blue-100 text-sm">
                      {item.description}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          </section>

          <div className="text-center mt-10">
            <p className="text-xl text-gray-700">Ready to simplify?</p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default About;
