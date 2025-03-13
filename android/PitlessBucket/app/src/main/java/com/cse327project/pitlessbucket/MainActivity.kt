package com.cse327project.pitlessbucket

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.toColorInt
import com.cse327project.pitlessbucket.ui.theme.PitlessBucketTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val fontFamily = FontFamily(
            Font(R.font.mplusrounded1c_thin, FontWeight.Thin),
            Font(R.font.mplusrounded1c_regular, FontWeight.Normal),
            Font(R.font.mplusrounded1c_medium, FontWeight.Medium),
            Font(R.font.mplusrounded1c_light, FontWeight.Light),
            Font(R.font.mplusrounded1c_extrabold, FontWeight.ExtraBold),
            Font(R.font.mplusrounded1c_bold, FontWeight.Bold),
            Font(R.font.mplusrounded1c_black, FontWeight.Black),

            )
        enableEdgeToEdge()
        setContent {
            PitlessBucketTheme {
                Column {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .fillMaxHeight(.11f)
                            .background(Color("#3182ce".toColorInt()))
                    ) {
                        Row(
                            modifier = Modifier
                                .padding(top = 50.dp, start = 10.dp)
                                .fillMaxWidth()
                        ) {
                            Text(
                                text = "Pitless Bucket",
                                fontFamily = fontFamily,
                                fontWeight = FontWeight.ExtraBold,
                                color = Color.White,
                                fontSize = 25.sp
                            )
                        }
                    }
                    Box (
                        modifier = Modifier
                            .fillMaxWidth()
                            .fillMaxHeight(.06f)
                            .background(Color.White),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text="Your Files & Folders",
                            fontWeight = FontWeight.Bold,
                            color = Color.Black,
                            fontSize = 20.sp,
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
        }
    }
}

