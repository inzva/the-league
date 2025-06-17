import { Container } from "@mui/material";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <Container>
      <article className="prose prose-invert max-w-none py-8">
        <h1>The League: Competitive Programming at Its Finest</h1>
        <p>
          Welcome to The League, an innovative competitive programming event
          that blends the excitement of esports with the intellectual challenge
          of algorithmic problem-solving. Designed to reignite the competitive
          spirit and foster team synergy, The League offers a dynamic platform
          for programmers of all levels to test their skills, strategize with
          teammates, and compete in an exciting format.
        </p>
        <h2>Purpose and Vision</h2>
        <p>
          The League was born from a desire to overcome the limitations of
          traditional problem solving competitions—such as the lack of team
          spirit, the misuse of AI tools, and a stagnant competitive atmosphere.
          Our mission is to create an environment where participants can:
        </p>
        <ul>
          <li>Build their own teams with friends they trust and vibe with.</li>
          <li>
            Experience the adrenaline of strategic, high-stakes competition.
          </li>
          <li>
            Showcase their problem-solving prowess in a fair and transparent
            setting.
          </li>
        </ul>
        <p>
          By incorporating elements from esports and emphasizing team dynamics,
          The League aims to deliver an unparalleled competitive experience
          that’s as fun to watch as it is to play.
        </p>
        <h2>How It Works</h2>
        <h3>Competition Format</h3>
        <p>
          The League follows a round-robin system, where every team faces off
          against all others in a series of matches spanning several months
          (September to March). Each match is a Best of 2 (Bo2) showdown:
        </p>
        <ul>
          <li>Teams compete over two problems.</li>
          <li>The team that wins the most problems takes the match.</li>
          <li>
            Ties are resolved using tiebreakers like the Neustadtl score or
            head-to-head results.
          </li>
        </ul>
        <p>
          The top teams advance to the playoffs, featuring a double-elimination
          bracket that gives everyone a fighting chance at the championship.
        </p>
        <h3>Pick and Ban System</h3>
        <p>
          A standout feature of The League is the Pick and Ban system, adding a
          strategic twist to the competition:
        </p>
        <ul>
          <li>
            Ban: Teams block problem categories they don’t want their opponents
            to tackle.
          </li>
          <li>Pick: Teams select problems that suit their strengths.</li>
        </ul>
        <p>
          This system, inspired by esports, uses icons for topics like Binary
          Search, Combinatorics, and Data Structures, displayed on a sleek
          interface. It forces teams to outsmart their rivals while showcasing
          their adaptability.
        </p>
        <h3>Winning Criteria</h3>
        <ul>
          <li>
            The first team to solve a problem correctly, within the time limit,
            and without plagiarism wins.
          </li>
          <li>
            If a team finishes early and places their balloon (optional signal),
            the opposing team gets 1 minute to solve the same problem for a
            draw—provided they’ve already solved the first problem.
          </li>
          <li>
            Matches are monitored live to ensure no AI tools are used,
            maintaining a level playing field.
          </li>
        </ul>
        <h3>Scoring</h3>
        <ul>
          <li>Win: 2 points</li>
          <li>Draw: 1 point</li>
          <li>Loss: 0 points</li>
        </ul>
        <p>
          In case of ties, head-to-head results or total wins take precedence,
          ensuring every match counts.
        </p>
        <h2>Team Dynamics</h2>
        <p>Teams are the heart of The League. Participants can:</p>
        <ul>
          <li>
            Form their own squads, choosing teammates they work well with.
          </li>
          <li>
            Include up to 1 substitute (stand-in) and 1 coach for tactical
            support.
          </li>
          <li>
            Use a stand-in up to 3 times per season if a teammate is unavailable
            (e.g., due to exams).
          </li>
        </ul>
        <p>
          Coaches analyze opponents and guide strategy, while substitutes keep
          the team flexible. Rosters must be finalized by the first week of
          September.
        </p>
        <h2>Schedule</h2>
        <p>
          Matches kick off in September and run through March, with key fixtures
          like:
        </p>
        <ul>
          <li>October: Team A vs. Team C, Team B vs. Team E, and more.</li>
          <li>November: Team A vs. Team D, Team C vs. Team G, etc.</li>
          <li>March: Early playoff qualifiers like Team A vs. Team B.</li>
        </ul>
        <p>
          The full schedule ensures regular action, culminating in a thrilling
          playoff phase.
        </p>
        <h2>Unique Features</h2>
        <p>
          The League integrates with the algoleague platform, enhancing the
          experience with:
        </p>
        <ul>
          <li>Team Pages: Custom profiles for each squad.</li>
          <li>Badges: Unique rewards for players.</li>
          <li>Leaderboard: Track standings in real-time.</li>
          <li>
            Live Monitoring: Matches are broadcasted and supervised to ensure
            fairness.
          </li>
          <li>Practice Mode: A mini-game version for off-season training.</li>
        </ul>
        <p>
          This ecosystem not only supports competitors but also engages
          spectators, making The League a community-driven event.
        </p>
        <h2>FAQs</h2>
        <h3>What if my teammate can’t play?</h3>
        <p>
          Notify us to bring in a stand-in (max 1 per match, 3 per season). They
          can’t be from an active opposing team.
        </p>
        <h3>Can we reschedule a match?</h3>
        <p>Yes, with approval from both teams—or use a stand-in.</p>
        <h3>What happens in a tiebreaker?</h3>
        <p>
          For two teams: Best of 3. For four or more: Round-robin, then
          Neustadtl score, head-to-head speed, or 1v1 matches.
        </p>
        <h3>Can I leave my seat during a match?</h3>
        <p>
          Only to stand, not to leave the camera’s view—unless there’s a
          technical issue.
        </p>
        <h2>Join The League</h2>
        <p>
          Whether you’re a veteran problem solver or a rising star, The League
          invites you to form your dream team, master the pick-and-ban strategy,
          and compete for glory. With a season full of challenges, surprises,
          and camaraderie, this is competitive programming redefined. Good luck,
          have fun!
        </p>
      </article>
    </Container>
  );
}
