import { useCallback, useEffect, useMemo, useState } from "react";
import { createJob, fetchJobs, Job } from "../api/client";

interface JobFormState {
  goal: string;
  sitePolicyInput: string;
}

const initialForm: JobFormState = {
  goal: "",
  sitePolicyInput: ""
};

const JobsPage = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [form, setForm] = useState<JobFormState>(initialForm);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadJobs = useCallback(async () => {
    setLoading(true);
    try {
      const data = await fetchJobs();
      setJobs(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load jobs");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadJobs();
  }, [loadJobs]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const sitePolicy = form.sitePolicyInput
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean);

    if (!form.goal || sitePolicy.length === 0) {
      setError("Provide both goal and at least one allowed domain.");
      return;
    }

    setLoading(true);
    try {
      await createJob({ goal: form.goal, site_policy: sitePolicy });
      setForm(initialForm);
      await loadJobs();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create job");
    } finally {
      setLoading(false);
    }
  };

  const jobRows = useMemo(
    () =>
      jobs.map((job) => (
        <tr key={job.id}>
          <td>
            <span className={`status-dot ${job.status === "completed" ? "ok" : "failed"}`} />
            {job.goal}
          </td>
          <td>{job.site_policy.join(", ")}</td>
          <td>{new Date(job.created_at).toLocaleString()}</td>
          <td>{job.status}</td>
        </tr>
      )),
    [jobs]
  );

  return (
    <div className="grid">
      <section className="card">
        <h2>New Job</h2>
        <form onSubmit={handleSubmit} className="grid">
          <label>
            Goal
            <input
              type="text"
              value={form.goal}
              onChange={(event) => setForm((prev) => ({ ...prev, goal: event.target.value }))}
            />
          </label>
          <label>
            Allowed domains (comma separated)
            <input
              type="text"
              value={form.sitePolicyInput}
              onChange={(event) =>
                setForm((prev) => ({ ...prev, sitePolicyInput: event.target.value }))
              }
            />
          </label>
          <div>
            <button type="submit" disabled={loading}>
              {loading ? "Submitting..." : "Create job"}
            </button>
          </div>
        </form>
        {error && <p style={{ color: "#f87171" }}>{error}</p>}
      </section>

      <section className="card">
        <h2>Jobs</h2>
        {loading && <p>Loading...</p>}
        {!loading && (
          <table>
            <thead>
              <tr>
                <th>Goal</th>
                <th>Allowed domains</th>
                <th>Created</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>{jobRows}</tbody>
          </table>
        )}
      </section>
    </div>
  );
};

export default JobsPage;
