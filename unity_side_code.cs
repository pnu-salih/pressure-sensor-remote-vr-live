using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using TMPro;
using System.Threading.Tasks;

public class PressureReceiver : MonoBehaviour
{
    public int serverPort = 9000;
    public TextMeshProUGUI pressureText;

    private TcpListener _listener;
    private string latestPressure = "";

    async void Start()
    {
        Debug.Log("PressureReceiver Start called");
        _listener = new TcpListener(IPAddress.Any, serverPort);
        _listener.Start();
        Debug.Log($"PressureReceiver listening on port {serverPort}");
        _ = AcceptLoop();
    }

    async Task AcceptLoop()
    {
        Debug.Log("AcceptLoop started");
        while (true)
        {
            Debug.Log("Waiting for client...");
            using (var client = await _listener.AcceptTcpClientAsync())
            using (var stream = client.GetStream())
            {
                Debug.Log("Client connected!");
                var buffer = new byte[256];
                while (true)
                {
                    int bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length);
                    if (bytesRead <= 0) break;
                    string pressure = Encoding.UTF8.GetString(buffer, 0, bytesRead).Trim();
                    latestPressure = pressure;
                    Debug.Log($"Received pressure: {pressure}");
                }
            }
        }
    }

    void Update()
    {
        if (!string.IsNullOrEmpty(latestPressure))
        {
            pressureText.text = $"Pressure: {latestPressure}";
        }
    }

    void OnDestroy()
    {
        _listener?.Stop();
    }
}

