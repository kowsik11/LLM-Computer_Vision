import { useCallback, useEffect, useState } from "react";
import { fetchRuns, Run } from "../api/client";

const RunDetailPage = () => {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadRuns = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchRuns();
      setRuns(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load runs");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadRuns();
  }, [loadRuns]);

  return (
    <section className="card">
      <h2>Runs</h2>
      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "#f87171" }}>{error}</p>}
      {!loading && runs.length === 0 && <p>No runs yet.</p>}
      {!loading && runs.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Run ID</th>
              <th>Job ID</th>
              <th>Status</th>
              <th>Started</th>
              <th>Finished</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr key={run.id}>
                <td>
                  <code>{run.id.slice(0, 8)}</code>
                </td>
                <td>{run.job_id}</td>
                <td>{run.status}</td>
                <td>{new Date(run.started_at).toLocaleString()}</td>
                <td>{run.finished_at ? new Date(run.finished_at).toLocaleString() : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
};

export default RunDetailPage;

