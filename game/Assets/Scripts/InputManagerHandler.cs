using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class InputManagerHandler : MonoBehaviour
{
    public Vector3[] hands;
    public GameObject[] handPointers;
    public int height;
    public int width;

    public void Start()
    {
        height = Screen.height;
        width = Screen.width;
    }

    public void Update()
    {
        for (int i=0; i<2; i++)
        {
            if (handPointers[i].activeSelf)
            {
                handPointers[i].transform.position = hands[i];

                Debug.Log(handPointers[i].transform.position.ToString());
            }
        }
    }

    public void SetPos(string handInfo)
    {
        bool isLeft;
        float x, y;

        string[] handInfoSplit = handInfo.Split('/');
        if (!bool.TryParse(handInfoSplit[0], out isLeft)){
            Debug.Log("SetPos > Type mismatch, isLeft is not bool type");
        }

        if (!float.TryParse(handInfoSplit[1], out x))
        {
            Debug.Log("SetPos > Type mismatch, x is not float type");
        }

        if (!float.TryParse(handInfoSplit[2], out y))
        {
            Debug.Log("SetPos > Type mismatch, y is not float type");
        }

        int handType = isLeft ? 0 : 1;
        hands[handType].x = (x - 0.5f) * 18;
        hands[handType].y = (y - 0.5f) * 14;
    }

    public void SetVisible(string handInfo)
    {
        bool isLeft;
        bool isVisible;

        string[] handInfoSplit = handInfo.Split('/');
        if (!bool.TryParse(handInfoSplit[0], out isLeft))
        {
            Debug.Log("SetPos > Type mismatch, isLeft is not bool type");
        }

        if (!bool.TryParse(handInfoSplit[0], out isVisible))
        {
            Debug.Log("SetPos > Type mismatch, isVisible is not bool type");
        }

        int handType = isLeft ? 0 : 1;
        handPointers[handType].SetActive(isVisible);
    }
}
