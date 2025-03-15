package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.InsertDriveFile
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.AddCard
import androidx.compose.material.icons.filled.AudioFile
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.HourglassEmpty
import androidx.compose.material.icons.filled.Image
import androidx.compose.material.icons.filled.PictureAsPdf
import androidx.compose.material.icons.filled.TextFormat
import androidx.compose.material.icons.filled.Upload
import androidx.compose.material.icons.filled.VideoFile
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.toColorInt
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.util.formatFileSize
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.DashboardState
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.FileInfo
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.fontFamily
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.signin_screen.UserData

@Composable
fun DashboardScreen(
    userData: UserData?,
    state: DashboardState,
    navController: NavController

    ){
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
                    fontSize = 25.sp,
                    modifier = Modifier
                        .clickable(onClick = { navController.navigate("dashboard")})
                )
                Spacer(modifier = Modifier
                    .fillMaxWidth(.7f))
                if(userData?.profilePictureUrl != null) {
                    AsyncImage(
                        model = userData.profilePictureUrl,
                        contentDescription = "Profile Picture",
                        modifier = Modifier
                            .size(40.dp)
                            .clip(CircleShape)
                            .clickable(onClick = { navController.navigate("profile")} ),
                        contentScale = ContentScale.Crop,
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(.06f)
                .background(Color.White),
            contentAlignment = Alignment.Center
        ) {
            Button(modifier = Modifier
                .fillMaxSize(),
                shape = RectangleShape,
                onClick = { navController.navigate("file_upload")}) {
                Icon(
                    imageVector = Icons.Filled.Upload,
                    contentDescription = "Upload Button",
                    modifier = Modifier
                        .size(25.dp))
                Text(
                    text = "Upload",
                    fontSize = 25.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(.04f)
                .background(Color.White),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "Your Files & Folders",
                fontWeight = FontWeight.Bold,
                color = Color.Black,
                fontSize = 20.sp,
                textAlign = TextAlign.Center
            )
        }
        Column {
//            if (userData != null) {
//                Text("Welcome, ${userData.username}")
//            }
            when {
                state.isLoading -> {
                    LoadingIndicator()
                }
                state.error != null -> {
//                    Text("Error: ${state.error}")
                    ErrorView(state.error) {
                        navController.navigate("dashboard")
                    }
                }
                else -> {
                    if (state.files.isEmpty()) {
                        EmptyFilesView()
                    } else {
                        FilesList(state.files)
                    }
                }
            }
        }
    }
}

@Composable
private fun LoadingIndicator() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

@Composable
private fun ErrorView(error: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Error: $error",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.error
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onRetry) {
            Text("Retry")
        }
    }
}

@Composable
private fun EmptyFilesView() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Filled.HourglassEmpty,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "No files available",
            style = MaterialTheme.typography.titleMedium
        )
    }
}

@Composable
private fun FilesList(files: List<FileInfo>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(items = files) { file ->
            FileItem(file = file)
        }
    }
}

@Composable
private fun FileItem(file: FileInfo) {
//    val formattedDate = remember(file.updated_at) {
//        val formatter = SimpleDateFormat("MMM dd, yyyy - HH:mm", Locale.getDefault())
//        formatter.format(file.updated_at)
//    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* Handle click */ },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // File type icon
            Icon(
                imageVector = when {
                    file.content_type.startsWith("image/") -> Icons.Filled.Image
                    file.content_type.startsWith("video/") -> Icons.Filled.VideoFile
                    file.content_type.startsWith("audio/") -> Icons.Filled.AudioFile
                    file.content_type.startsWith("text/") -> Icons.Filled.TextFormat
                    file.content_type.startsWith("application/pdf") -> Icons.Filled.PictureAsPdf
                    else -> Icons.AutoMirrored.Filled.InsertDriveFile
                },
                contentDescription = null,
                modifier = Modifier.size(40.dp),
                tint = MaterialTheme.colorScheme.primary
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = file.file_name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )

                Spacer(modifier = Modifier.height(4.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = file.size.formatFileSize(),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.outline
                    )

//                    Text(
//                        text = formattedDate,
//                        style = MaterialTheme.typography.bodySmall,
//                        color = MaterialTheme.colorScheme.outline
//                    )
                }
            }
        }
    }
}