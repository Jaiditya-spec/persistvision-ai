function Dashboard() {

  const cards = [
    {
      title: "Overall Persistency",
      value: "28.64%"
    },
    {
      title: "Savings",
      value: "29.17%"
    },
    {
      title: "Protection",
      value: "28.57%"
    },
    {
      title: "Policies",
      value: "1,500"
    }
  ];

  return (
    <div className="dashboard">

      {cards.map((card, index) => (

        <div
          key={index}
          className="card"
        >
          <h3>{card.title}</h3>
          <h1>{card.value}</h1>
        </div>

      ))}

    </div>
  );
}

export default Dashboard;